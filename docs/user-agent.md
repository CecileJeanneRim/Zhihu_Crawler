
# user agent
## header
## User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
## Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。
## application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
## application/json ： 在 JSON RPC 调用时使用
## application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
## 在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务
