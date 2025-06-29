#ifndef WIFICAM_HPP
#define WIFICAM_HPP

#include <esp32cam.h>
#include <WebServer.h>

// Variáveis externas
extern esp32cam::Resolution initialResolution; // Resolução inicial da câmera
extern WebServer server; // Objeto do servidor HTTP

// Definição do pino do flash
#define FLASH_PIN 4

// Protótipo da função para adicionar manipuladores de requisições
void addRequestHandlers();

#endif // WIFICAM_HPP
