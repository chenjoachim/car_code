
#include <SPI.h>
#include <MFRC522.h>
// 引入 SPI 程式庫 與 MFRC522 程式庫
#define RST_PIN 13
#define SDA_PIN 9
// 設定重設腳位 與 SPI 介面裝置選擇腳位
MFRC522 *mfrc522;
// 宣告MFRC522指標
void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522 = new MFRC522(SDA_PIN, RST_PIN);
  // 請系統去要一塊記憶體空間，後面呼叫它的建構函式
  // 將(SS, RST) 當成參數傳進去初始化。
  mfrc522->PCD_Init();
  /* 初始化MFRC522讀卡機 PCD_Init 模組。 -> 表示：
  透過記憶體位置，找到 mfrc522 這物件，再翻其內容。*/
  Serial.println(F("Read UID on a MIFARE PICC:"));
}

void loop() { //檢查是否讀取到RFID, 對應的UID 是什麼？
  if(!mfrc522->PICC_IsNewCardPresent()) {
    goto FuncEnd;
   } //PICC_IsNewCardPresent()：是否感應到新的卡片?
   if(!mfrc522->PICC_ReadCardSerial()) {
    goto FuncEnd;
   } //PICC_ReadCardSerial()：是否成功讀取資料?
   Serial.println(F("**Card Detected:**"));
   mfrc522->PICC_DumpDetailsToSerial(&(mfrc522->uid)); //讀出 UID
   mfrc522->PICC_HaltA(); // 讓同一張卡片進入停止模式 (只顯示一次)
   mfrc522->PCD_StopCrypto1(); // 停止 Crypto1
   FuncEnd:; // goto 跳到這.
}
