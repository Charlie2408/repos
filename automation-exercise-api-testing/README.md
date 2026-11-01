# Automation Exercise 电商平台接口测试项目

基于 **Postman + Collection Runner** 对自动化测试练习平台 [Automation Exercise](https://automationexercise.com/) 提供的 REST API 开展接口测试，覆盖商品搜索、用户注册、登录、用户资料增改查等核心接口，作为软件测试实习简历中的实战项目。

## 一、项目文件

| 文件 | 说明 |
|---|---|
| `automationexercise_api_test.json` | Postman Collection，可直接导入 Postman 运行 |
| `Automation Exercise 测试用例记录.xlsx` | 接口测试用例设计与执行记录 |

## 二、覆盖接口

| 接口 | 方法 | 用例 |
|---|---|---|
| `/api/searchProduct` 商品搜索 | POST | 正常流（top 关键词）/ 空关键词异常流 |
| `/api/createAccount` 注册用户 | POST | 邮箱已存在异常流 |
| `/api/verifyLogin` 登录 | POST | 正确账号密码 / 错误密码 / 缺 email 参数 |
| `/api/createAccount` 更新用户资料 | POST | 正常流 |
| `/api/getUserDetailByEmail` 查询用户详情 | GET | 正常流 |

## 三、运行方式

1. 打开 Postman → `Import` → 选择 `automationexercise_api_test.json` 导入 Collection
2. 选中该 Collection → 点击 `Run` 进入 Collection Runner
3. 批量执行并查看断言通过情况（每个接口均含 **HTTP 状态码 + 响应体字段** 双重断言）

## 四、测试设计方法

- **等价类划分**：正常参数 / 异常参数分类设计用例
- **正反向用例**：正确账号密码（正向）vs 错误密码 / 缺参（反向）
- **双层断言**：HTTP 状态码 + 响应 JSON 字段校验，提升用例有效性

> 说明：collection 中使用的邮箱为自建测试账号（`charlie_test_*@test.com`），非真实用户数据。
