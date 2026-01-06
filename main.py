import os
import time
import pandas as pd
import google.generativeai as genai
from io import StringIO

# =配置区域=====
# TODO: 替换为实际的 API Key
API_KEY = "YOUR_GEMINI_API_KEY"
IMAGE_FOLDER = "./lab_images"
OUTPUT_FILE = "batch_results.csv"

# 配置 Gemini
genai.configure(api_key=API_KEY)

# 使用 Flash 模型平衡速度与成本
model = genai.GenerativeModel('gemini-1.5-flash')

# 核心提示词 (System Prompt)
PROMPT = """
请分析这张医学化验单图片。

任务：
1. 提取其中的表格数据。
2. 直接输出为严格的 CSV 格式（逗号分隔）。
3. 必须包含以下表头：Source_File, 项目名称, 结果, 参考区间, 单位, 异常标记(High/Low/箭头)。
4. 如果某项为空，留空即可。
5. 不要输出任何 Markdown 标记（如 ```csv），只输出纯文本数据。
6. 如果图片模糊或无法识别，输出 "ERROR"。
"""

def process_images():
    all_data = []
    
    # 检查输入目录
    if not os.path.exists(IMAGE_FOLDER):
        print(f"错误: 文件夹 {IMAGE_FOLDER} 不存在")
        return

    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"检测到 {len(image_files)} 张图片，开始处理...")

    for filename in image_files:
        filepath = os.path.join(IMAGE_FOLDER, filename)
        print(f"正在处理: {filename} ...", end="")

        try:
            # Upload & Generate
            sample_file = genai.upload_file(path=filepath, display_name=filename)
            response = model.generate_content([PROMPT, sample_file])
            content = response.text.strip()
            
            if "ERROR" in content or not content:
                print(" -> 无法识别或空结果")
                continue

            # Parse CSV
            # 使用 on_bad_lines='skip' 防止格式错误导致整个脚本中断
            df = pd.read_csv(StringIO(content), on_bad_lines='skip')
            
            # 添加文件名列用于溯源 (如果API没按要求返回Source_File列，强制覆盖)
            df['Source_File'] = filename
            
            all_data.append(df)
            print(" -> 成功")
            
            # Rate Limit Protection
            time.sleep(2)

        except Exception as e:
            print(f" -> 失败: {str(e)}")

    # Merge & Save
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        # utf-8-sig 用于兼容 Excel 打开中文不乱码
        final_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n处理完成！所有数据已保存至: {OUTPUT_FILE}")
    else:
        print("\n未提取到有效数据。")

if __name__ == "__main__":
    process_images()
