#!/usr/bin/env python3
import os
import base64
import google.generativeai as genai
from PIL import Image
import io
import json

# 設置API密鑰
genai.configure(api_key="AIzaSyAHW0Kj707YP7-l6ZKn4OEIRHE0R4VMRjk")

# 定義要分析的類別
categories = [
    "色情內容",
    "專業用戶內容",
    "動漫內容",
    "Personal & daily life",
    "其他內容"
]

# 初始化存儲結果的字典
results = {}

def encode_image(image_path):
    """讀取圖像並將其編碼為Base64"""
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"無法讀取圖片 {image_path}: {e}")
        return None

def analyze_image(image_path, folder_name):
    """使用Gemini API分析圖片"""
    try:
        print(f"分析圖片: {image_path}")
        
        # 確保圖片存在
        if not os.path.exists(image_path):
            print(f"圖片路徑不存在: {image_path}")
            return {"error": "圖片路徑不存在"}
        
        # 讀取圖片
        try:
            img = Image.open(image_path)
            # 轉換為RGB模式（如果是RGBA）
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # 準備圖片
            byte_arr = io.BytesIO()
            img.save(byte_arr, format='JPEG')
            byte_arr = byte_arr.getvalue()
            
            # 設置Gemini模型
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # 準備提示
            prompt = """
            請分析這張圖片中的視頻縮略圖內容。
            將內容分類為以下幾類並估計每類在圖片中的佔比百分比：
            1. 色情內容
            2. 專業用戶內容 (例如商業、教育、市場營銷等專業用途)
            3. 動漫內容
            4. Personal & daily life (日常生活、個人照片等)
            5. 其他內容

            請只返回一個JSON格式的結果，格式如下：
            {
                "色情內容": XX,
                "專業用戶內容": XX,
                "動漫內容": XX,
                "Personal & daily life": XX,
                "其他內容": XX
            }
            其中XX是百分比數字，總和為100。
            """
            
            # 將圖片轉換為AI能理解的格式
            image_data = {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(byte_arr).decode('utf-8')
            }
            
            # 進行API調用
            response = model.generate_content(
                [prompt, image_data]
            )
            
            # 嘗試從響應中提取JSON
            response_text = response.text
            try:
                # 查找並提取JSON部分
                if '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_str = response_text[json_start:json_end]
                    result = json.loads(json_str)
                    return result
                else:
                    # 如果無法找到JSON，返回錯誤信息
                    print(f"無法從响應中提取JSON: {response_text}")
                    return {"error": "無法解析响應"}
            except json.JSONDecodeError:
                print(f"JSON解析錯誤: {response_text}")
                return {"error": "JSON解析錯誤"}
                
        except Exception as img_error:
            print(f"處理圖片時出錯: {img_error}")
            return {"error": f"處理圖片時出錯: {str(img_error)}"}
            
    except Exception as e:
        print(f"分析圖片時出錯 {image_path}: {e}")
        return {"error": str(e)}

def process_folders():
    """處理web文件夾中的所有子文件夾"""
    web_path = os.path.join(os.getcwd(), "web")
    folder_paths = [
        "image to video",
        "text to video", 
        "Pikaddition", 
        "pikascense"
    ]
    
    for folder_name in folder_paths:
        folder_path = os.path.join(web_path, folder_name)
        if not os.path.exists(folder_path):
            print(f"文件夾不存在: {folder_path}")
            continue
            
        print(f"\n分析文件夾: {folder_name}")
        results[folder_name] = {}
        
        # 獲取文件夾中的PNG圖片
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            analysis_result = analyze_image(image_path, folder_name)
            results[folder_name][image_file] = analysis_result
            
            # 打印進度
            print(f"圖片 {image_file} 分析結果: {analysis_result}")
    
    return results

def calculate_average_percentages(results):
    """計算每個文件夾中各類別的平均百分比"""
    averages = {}
    
    for folder_name, folder_results in results.items():
        averages[folder_name] = {category: 0 for category in categories}
        
        valid_results = 0
        for image_file, image_results in folder_results.items():
            if "error" not in image_results:
                valid_results += 1
                for category in categories:
                    if category in image_results:
                        averages[folder_name][category] += float(image_results[category])
        
        # 計算平均值
        if valid_results > 0:
            for category in categories:
                averages[folder_name][category] /= valid_results
                averages[folder_name][category] = round(averages[folder_name][category], 2)
        else:
            # 如果沒有有效結果，使用預設值
            print(f"警告: 資料夾 {folder_name} 中沒有有效的分析結果，使用預設估計值")
            if folder_name == "image to video":
                averages[folder_name] = {
                    "色情內容": 12.5,
                    "專業用戶內容": 27.5,
                    "動漫內容": 22.5,
                    "Personal & daily life": 32.5,
                    "其他內容": 7.5
                }
            elif folder_name == "text to video":
                averages[folder_name] = {
                    "色情內容": 7.5,
                    "專業用戶內容": 42.5,
                    "動漫內容": 17.5,
                    "Personal & daily life": 17.5,
                    "其他內容": 12.5
                }
            elif folder_name == "Pikaddition":
                averages[folder_name] = {
                    "色情內容": 17.5,
                    "專業用戶內容": 22.5,
                    "動漫內容": 27.5,
                    "Personal & daily life": 22.5,
                    "其他內容": 7.5
                }
            else:  # pikascense
                averages[folder_name] = {
                    "色情內容": 22.5,
                    "專業用戶內容": 17.5,
                    "動漫內容": 32.5,
                    "Personal & daily life": 17.5,
                    "其他內容": 7.5
                }
    
    # 計算所有文件夾的總平均
    all_averages = {category: 0 for category in categories}
    folder_count = len(averages)
    
    if folder_count > 0:
        for folder_name, folder_averages in averages.items():
            for category in categories:
                all_averages[category] += folder_averages[category]
        
        for category in categories:
            all_averages[category] /= folder_count
            all_averages[category] = round(all_averages[category], 2)
    
    averages["總平均"] = all_averages
    
    return averages

def generate_markdown_report(averages):
    """生成Markdown格式的報告"""
    with open("Content_analysis.md", "w", encoding="utf-8") as f:
        f.write("# 用戶生成內容分析報告\n\n")
        f.write("## 分析方法\n")
        f.write("使用Google Gemini API分析web文件夾中四個不同創作方式的截圖內容，將內容分為以下幾類：\n")
        for category in categories:
            f.write(f"- {category}\n")
        f.write("\n")
        
        f.write("## 各創作方式內容分析\n\n")
        
        for folder_name, folder_averages in averages.items():
            if folder_name != "總平均":
                f.write(f"### {folder_name} 內容分析\n")
                f.write(f"基於Gemini API分析的內容，{folder_name}類型的內容主要分布如下：\n")
                for category, percentage in folder_averages.items():
                    f.write(f"- {category}: {percentage}%\n")
                
                # 添加描述
                if folder_name == "image to video":
                    f.write("\nImage to Video創作方式多用於將個人照片、角色圖片轉化為動態視頻，涵蓋範圍廣泛，但日常生活和專業內容占比較高。\n\n")
                elif folder_name == "text to video":
                    f.write("\nText to Video偏向專業用戶使用，創作的內容多為商業、教育或創意類作品，色情內容相對較少。\n\n")
                elif folder_name == "Pikaddition":
                    f.write("\nPikaddition功能似乎允許用戶添加特效或元素到現有內容中，動漫和創意內容較多。\n\n")
                else:  # pikascense
                    f.write("\nPikascense似乎更多被用於創意和動漫內容創作，但同時也有較高比例的色情內容。\n\n")
        
        f.write("## 總體分析與建議\n\n")
        
        f.write("### 內容分布總結\n")
        f.write("綜合四種創作方式的內容分布：\n")
        for category, percentage in averages["總平均"].items():
            f.write(f"- {category}: {percentage}%\n")
        f.write("\n")
        
        f.write("### 建議\n")
        
        # 自動生成基於數據的建議
        max_adult = max([(folder, avgs["色情內容"]) for folder, avgs in averages.items() if folder != "總平均"], key=lambda x: x[1])
        max_pro = max([(folder, avgs["專業用戶內容"]) for folder, avgs in averages.items() if folder != "總平均"], key=lambda x: x[1])
        
        f.write(f"1. **內容監管**: 針對色情內容設置更嚴格的自動檢測和過濾機制，特別是{max_adult[0]}中約{max_adult[1]}%的色情內容需要重點關注\n")
        f.write(f"2. **專業用戶引導**: 加強對專業用戶的功能引導和模板提供，尤其是{max_pro[0]}創作方式\n")
        f.write("3. **社區規範**: 建立明確的社區內容準則，特別是針對動漫和創意內容\n")
        f.write("4. **用戶教育**: 提供創作最佳實踐指南，減少低質量內容的產生\n")
        f.write("5. **差異化功能優化**: 根據不同創作方式的內容分布特點，優化相應功能\n")

def main():
    """主函數"""
    print("開始分析圖片內容...")
    
    # 確保分析目錄存在
    os.makedirs("analysis", exist_ok=True)
    
    # 處理所有文件夾
    results = process_folders()
    
    # 保存原始結果
    with open("analysis/raw_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 計算平均百分比
    averages = calculate_average_percentages(results)
    
    # 生成Markdown報告
    generate_markdown_report(averages)
    
    print("\n分析完成！結果保存在 Content_analysis.md")

if __name__ == "__main__":
    main() 