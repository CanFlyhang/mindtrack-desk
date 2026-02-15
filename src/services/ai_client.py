import os
from volcenginesdkarkruntime import Ark
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ArkClient:
    def __init__(self):
        self.api_key = os.getenv("ARK_API_KEY")
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3"
        self.model = os.getenv("ARK_MODEL_NAME", "doubao-pro-4k-vision")
        self.client = None
        if not self.api_key:
            print("Warning: ARK_API_KEY not found in environment variables.")
        else:
            self.client = Ark(
                base_url=self.base_url,
                api_key=self.api_key
            )

    def analyze_image(self, base64_image, prompt="请简要总结屏幕截图中的内容，识别当前正在进行的任务。"):
        if not self.api_key or self.client is None:
            return "错误: 未配置 API Key"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url", 
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {e}")
            return f"分析失败: {str(e)}"
