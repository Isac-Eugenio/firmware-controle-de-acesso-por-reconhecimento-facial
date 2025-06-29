#include "WifiCam.hpp"
#include <WiFi.h>

// Redes Wi-Fi
static const char* WIFI_SSID_1 = "NETWORK_FOR_IOT";
static const char* WIFI_PASS_1 = "Automation33";
static const IPAddress IP_1(10, 0, 0, 120);
static const IPAddress GATEWAY_1(10, 0, 0, 1);
static const IPAddress SUBNET_1(255, 255, 255, 0);

static const char* WIFI_SSID_2 = "Familiabuscape";
static const char* WIFI_PASS_2 = "Elephant33";
static const IPAddress IP_2(192, 168, 0, 20);
static const IPAddress GATEWAY_2(192, 168, 0, 1);
static const IPAddress SUBNET_2(255, 255, 255, 0);

esp32cam::Resolution initialResolution;
WebServer server(80);

bool connectToWiFi(const char* ssid, const char* password, IPAddress ip, IPAddress gateway, IPAddress subnet, int timeout = 10000) {
  WiFi.disconnect();
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  Serial.printf("Connecting to WiFi: %s...\n", ssid);
  
  unsigned long startAttempt = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttempt < timeout) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("Connected to %s with IP: %s\n", ssid, WiFi.localIP().toString().c_str());
    return true;
  } else {
    Serial.printf("Failed to connect to %s\n", ssid);
    return false;
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  delay(1000);

  pinMode(FLASH_PIN, OUTPUT);
  digitalWrite(FLASH_PIN, 0);

  // Tentativa de conexão com as redes
  if (!connectToWiFi(WIFI_SSID_1, WIFI_PASS_1, IP_1, GATEWAY_1, SUBNET_1, 10000)) {
    if (!connectToWiFi(WIFI_SSID_2, WIFI_PASS_2, IP_2, GATEWAY_2, SUBNET_2, 10000)) {
      Serial.println("All WiFi connection attempts failed. Restarting...");
      delay(5000);
      ESP.restart();
    }
  }

  // Inicialização da câmera
  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("Camera initialization failed");
      delay(5000);
      ESP.restart();
    }
    Serial.println("Camera initialized successfully");
  }

  Serial.println("Camera starting");
  Serial.printf("http://%s\n", WiFi.localIP().toString().c_str());

  addRequestHandlers();
  server.begin();
}

void loop() {
  server.handleClient();
}
