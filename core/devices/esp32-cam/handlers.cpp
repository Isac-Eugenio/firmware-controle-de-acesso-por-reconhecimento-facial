#include "WifiCam.hpp"
#include <StreamString.h>
#include <uri/UriBraces.h>

// Página inicial HTML
static const char FRONTPAGE[] = R"EOT(
<!doctype html>
<title>esp32cam WifiCam example</title>
<style>
  table,th,td { border: solid 1px #000000; border-collapse: collapse; }
  th,td { padding: 0.4rem; }
  a { text-decoration: none; }
  footer { margin-top: 1rem; }
</style>
<body>
<h1>esp32cam WifiCam example</h1>
<table>
  <thead>
    <tr><th>BMP<th>JPG<th>MJPEG
  <tbody id="resolutions">
    <tr><td colspan="3">loading
</table>
<footer>Powered by <a href="https://esp32cam.yoursunny.dev/">esp32cam</a></footer>
<script type="module">
  async function fetchText(uri, init) {
    const response = await fetch(uri, init);
    if (!response.ok) {
      throw new Error(await response.text());
    }
    return (await response.text()).trim().replaceAll("\r\n", "\n");
  }

  try {
    const list = (await fetchText("/resolutions.csv")).split("\n");
    document.querySelector("#resolutions").innerHTML = list.map((r) => `<tr>${
      ["bmp", "jpg", "mjpeg"].map((fmt) => `<td><a href="/${r}.${fmt}">${r}</a>`).join("")
    }`).join("");
  } catch (err) {
    document.querySelector("#resolutions td").textContent = err.toString();
  }
</script>
)EOT";

// Função para capturar imagens (com controle do flash)
static void serveStill(bool wantBmp) {
  digitalWrite(FLASH_PIN, HIGH); // Liga o flash
  delay(1000); // Mantém o flash ligado por 3 segundos

  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("capture() failure");
    server.send(500, "text/plain", "still capture error\n");
    digitalWrite(FLASH_PIN, LOW); // Desliga o flash em caso de erro
    return;
  }

  Serial.printf("capture() success: %dx%d %zub\n", frame->getWidth(), frame->getHeight(), frame->size());

  if (wantBmp) {
    if (!frame->toBmp()) {
      Serial.println("toBmp() failure");
      server.send(500, "text/plain", "convert to BMP error\n");
      digitalWrite(FLASH_PIN, LOW); // Desliga o flash em caso de erro
      return;
    }
    Serial.printf("toBmp() success: %dx%d %zub\n", frame->getWidth(), frame->getHeight(), frame->size());
  }

  server.setContentLength(frame->size());
  server.send(200, wantBmp ? "image/bmp" : "image/jpeg");
  frame->writeTo(server.client());

  digitalWrite(FLASH_PIN, LOW); // Desliga o flash após captura
}

// Função para transmitir vídeo em streaming (mantém o flash ligado)
static void serveMjpeg() {
  Serial.println("MJPEG streaming begin");
  digitalWrite(FLASH_PIN, HIGH); // Liga o flash durante o streaming

  auto startTime = millis();
  int nFrames = esp32cam::Camera.streamMjpeg(server.client());
  auto duration = millis() - startTime;

  digitalWrite(FLASH_PIN, LOW); // Desliga o flash após o streaming
  Serial.printf("MJPEG streaming end: %dfrm %0.2ffps\n", nFrames, 1000.0 * nFrames / duration);
}

// Adiciona os manipuladores de requisições
void addRequestHandlers() {
  server.on("/", HTTP_GET, [] {
    server.setContentLength(sizeof(FRONTPAGE));
    server.send(200, "text/html");
    server.sendContent(FRONTPAGE, sizeof(FRONTPAGE));
  });

  server.on("/robots.txt", HTTP_GET, [] {
    server.send(200, "text/html", "User-Agent: *\nDisallow: /\n");
  });

  server.on("/resolutions.csv", HTTP_GET, [] {
    StreamString b;
    for (const auto& r : esp32cam::Camera.listResolutions()) {
      b.println(r);
    }
    server.send(200, "text/csv", b);
  });

  server.on(UriBraces("/{}x{}.{}"), HTTP_GET, [] {
    long width = server.pathArg(0).toInt();
    long height = server.pathArg(1).toInt();
    String format = server.pathArg(2);
    if (width == 0 || height == 0 || !(format == "bmp" || format == "jpg" || format == "mjpeg")) {
      server.send(404);
      return;
    }

    auto r = esp32cam::Camera.listResolutions().find(width, height);
    if (!r.isValid()) {
      server.send(404, "text/plain", "non-existent resolution\n");
      return;
    }
    if (r.getWidth() != width || r.getHeight() != height) {
      server.sendHeader("Location", String("/") + r.getWidth() + "x" + r.getHeight() + "." + format);
      server.send(302);
      return;
    }

    if (!esp32cam::Camera.changeResolution(r)) {
      Serial.printf("changeResolution(%ld,%ld) failure\n", width, height);
      server.send(500, "text/plain", "changeResolution error\n");
    }
    Serial.printf("changeResolution(%ld,%ld) success\n", width, height);

    if (format == "bmp") {
      serveStill(true);
    } else if (format == "jpg") {
      serveStill(false);
    } else if (format == "mjpeg") {
      serveMjpeg();
    }
  });
}
