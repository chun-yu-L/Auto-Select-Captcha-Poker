# Anti-Poker
此 Python 程式利用 Selenium 和 OpenCV 函式庫自動解開撲克牌反爬蟲機制。它透過以下步驟來實現：

## 安裝依賴項
請確保已安裝以下依賴項，可以運行以下命令來安裝:
```bash
pip install -r requirements.txt
```

## anti_poker.py
anti_poker.py 檔案包含了解決撲克牌圖像比對問題的核心邏輯。它定義了一個 AntiPoker 類別，提供了以下功能:

1.  從網頁抓取圖像:
    - 使用 Selenium 從網頁上抓取撲克牌圖像。
    - 將圖像垂直分割成左右兩半。

2. 計算圖像相似度:
    - 使用 OpenCV 計算目標圖像與可選圖像之間的相似度。
    - 找出最相似的兩張牌。
3. 自動化操作:
    - 自動點擊選擇最相似的牌。
    - 提交選擇結果。
    - 提供 `fail_to_solve()` 方法,用於重新嘗試解題。

## 使用方式
詳細使用範例參考 example.ipynb
1. 確保已下載並設置好 Selenium 所需的 WebDriver (例如 ChromeDriver)。
2. 在 Python 中導入 AntiPoker 類別並使用
    ```python
    from anti_poker import AntiPoker
    from selenium import webdriver

    driver = webdriver.Chrome()  # 或使用其他 WebDriver
    anti_poker = AntiPoker(driver)
    anti_poker.solve_poker()
    anti_poker.click_result(anti_poker.result_indices)
    anti_poker.submit()
    ```
3. 如果選擇錯誤，可以使用 `anti_poker.fail_to_solve()` 方法來重新嘗試。

**注意**: 此程式專為特定的撲克牌防駭驗證碼實作而設計，對於不同的驗證碼變體可能需要進行調整。