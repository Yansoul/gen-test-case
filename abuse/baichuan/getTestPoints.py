import json
import re

def extract_test_points_from_str(input_str):
    # 使用正则表达式查找 JSON 数据
    json_str_match = re.search(r'```json([\s\S]*?)```', input_str)
    if not json_str_match:
        raise ValueError("JSON data not found in the input string")

    json_str = json_str_match.group(1)  # 提取 JSON 字符串
    # 移除前后的换行符并转义特殊字符
    json_str = json_str.strip().replace('\n', '\\n').replace('\t', '\\t')

    # 尝试解析 JSON 字符串
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON data: {e}")

    # 提取所有测试点
    test_points = []
    for item in data["test_points"]:
        category = item["category"]
        content = item["content"]
        test_points.append({"category": category, "content": content})

    return test_points


# 示例字符串
input_str = '''
"content":"根据您提供的信息，我为您生成了以下测试点：
\n\n```json\n{\n  \"test_points\": [\n    
{\n      \"category\": \"连通性验证\",\n      
\"content\": \"检查服务器端接口是否正常启动，客户端
是否能够建立连接并发送请求到服务器\"\n    },\n    
{\n      \"category\": \"单字段验证\",\n      
\"content\": \"字段custNbr，检查存在性、正确的类型
以及是否在预期的长度范围内\"\n    },\n    {\n      
\"category\": \"单字段验证\",\n      \"content\"
: \"字段crdAcNbr，检查存在性、正确的类型以及是否在预期的长
度范围内\"\n    },\n    {\n      \"category\"
: \"单字段验证\",\n      \"content\": \"字段crd
AcType，检查存在性、正确的类型以及是否在预期的长度范围内
\"\n    },\n    {\n      \"category\": \"单字
段验证\",\n      \"content\": \"字段idType，检查存
在性、正确的类型以及是否在预期的长度范围内\"\n    },\n 
   {\n      \"category\": \"单字段验证\",\n     
    \"content\": \"字段idNbr，检查存在性、正确的类型
    以及是否在预期的长度范围内\"\n    },\n    {\n   
       \"category\": \"单字段验证\",\n      \"co
       ntent\": \"字段ownBrorg，检查存在性、正确的类型
       以及是否在预期的长度范围内\"\n    },\n    {\n  
           \"category\": \"单字段验证\",\n      \"c
           ontent\": \"字段pageSize，检查存在性、正确
           的类型以及是否在预期的长度范围内\"\n    },\n
               {\n      \"category\": \"单字段验证\
               ",\n      \"content\": \"字段curren
               tPage，检查存在性、正确的类型以及是否在预期的长
               度范围内\"\n    },\n    {\n      \"catego
               ry\": \"字段间规则验证\",\n      \"content\": \"字段custNbr、crdA
               cNbr、idNbr，检查至少有一个字段是必填的\"\n    },\n    {\n      \"category\": \
               "字段间规则验证\",\n      \"content\": \"字段crdAcNbr和crdAcType，检查当crdAcNbr为必填时，
               crdAcType也为必填\"\n    },\n    {\n      \"category\": \"字段间规则验证\",\n      \"content\": 
               \"字段idType和idNbr，检查当idNbr为必填时，idType也为必填\"\n    }\n  ]
               \n}\n```\n\n这个测试点列表涵盖了连通性验证、单字段验证和字段间规则验证。每个
               测试点的具体内容都涉及到了接口定义中的参数。"}
'''

try:
    test_points = extract_test_points_from_str(input_str)
    for point in test_points:
        print(f"Category: {point['category']}, Content: {point['content']}")
except ValueError as e:
    print(e)
