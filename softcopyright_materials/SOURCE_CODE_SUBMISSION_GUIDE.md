# 源程序提交指南

本文件用于整理软著申报时的源程序提交材料。

## 1. 规则依据

依据《计算机软件著作权登记办法》：

- 第九条：申请软件著作权登记，应向中国版权保护中心提交申请表、软件鉴别材料和相关证明文件。
- 第十条：软件鉴别材料包括程序和文档的鉴别材料。程序和文档的鉴别材料应由源程序和任何一种文档前、后各连续 30 页组成。整个程序和文档不到 60 页的，应提交整个源程序和文档。除特定情况外，程序每页不少于 50 行，文档每页不少于 30 行。
- 第十七条：申请表应使用中文填写，申请登记的文件应使用国际标准 A4 纸张。

官方来源：

- 国家版权局《计算机软件著作权登记办法》
  - [国家版权局 PDF（2024 汇编版）](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/P020241015604759788122.pdf)
  - 关键条款见第 9 至第 17 条

## 2. 当前项目源码统计

以下统计已排除 `.venv`、`node_modules`、`dist`、图片资源和锁文件，只保留当前项目中适合用于软著申报的核心源程序。

- 核心文件数：`18`
- 核心代码总行数：`1915`

结论：

按常见排版方式，`1915` 行代码通常不足 `60` 页程序页，因此这个项目更适合直接提交全部核心源程序，而不是只提交前后各 30 页。

## 3. 建议提交范围

建议提交以下全部核心源程序：

### 3.1 后端

1. `save_tears_backend/main.py`
2. `save_tears_backend/api.py`
3. `save_tears_backend/test.py`

### 3.2 小程序核心

4. `save_tears_miniprogram/src/main.ts`
5. `save_tears_miniprogram/src/App.vue`
6. `save_tears_miniprogram/src/api/index.ts`
7. `save_tears_miniprogram/src/pages/login/index.vue`
8. `save_tears_miniprogram/src/pages/register/index.vue`
9. `save_tears_miniprogram/src/pages/home/index.vue`
10. `save_tears_miniprogram/src/pages/profile/index.vue`
11. `save_tears_miniprogram/src/pages/admin/index.vue`
12. `save_tears_miniprogram/src/pages/water-flow/index.vue`
13. `save_tears_miniprogram/src/pages/sewage-turbidity/index.vue`
14. `save_tears_miniprogram/src/pages/water-bill/index.vue`
15. `save_tears_miniprogram/src/pages/index/index.vue`
16. `save_tears_miniprogram/src/uni.scss`
17. `save_tears_miniprogram/src/env.d.ts`
18. `save_tears_miniprogram/src/shime-uni.d.ts`

## 4. 不建议提交的内容

以下内容一般不建议放入软著源程序提交件：

1. 虚拟环境目录，例如 `.venv/`
2. 依赖目录，例如 `node_modules/`
3. 构建产物，例如 `dist/`
4. 图片、Logo、背景图等静态资源
5. `package-lock.json` 等锁文件
6. `README.md`、交接文档、PPT、部署说明等非程序文件

原因：

这些内容不是你主张著作权的核心原创程序，加入后只会增加排版负担，还可能稀释项目业务逻辑。

## 5. 建议排序

为了让审查人员更容易理解系统结构，建议按下面顺序排版源码：

1. 后端入口 `main.py`
2. 后端接口 `api.py`
3. 小程序入口 `main.ts`
4. 小程序根组件 `App.vue`
5. 小程序接口封装 `src/api/index.ts`
6. 注册登录页面
7. 首页与个人中心页面
8. 管理页面
9. 用水、污水、账单页面
10. 其余辅助文件

如果你最终制作 PDF，建议每个文件开始前加一行文件路径标题，例如：

```text
// File: save_tears_backend/api.py
```

这样更利于阅读和归档。

## 6. 页数控制建议

如果你把全部核心源程序直接排版成 A4 PDF，建议遵循以下做法：

1. 每页 50 行左右
2. 字体使用等宽字体，例如 `Courier New`、`Consolas`
3. 字号建议 `9pt` 到 `10.5pt`
4. 页眉标注软件名称和版本号，例如 `Save Tears 节水管理系统 V1.0`
5. 页脚标注页码

按 `1915` 行估算：

- 约 `39` 页程序页可覆盖全部核心源码

这意味着：

- 你完全可以交“完整源程序”
- 没有必要为了凑页数去加入依赖文件或自动生成文件

## 7. 如果代理坚持做成 60 页

如果代理机构或打印模板固定要求做成 60 页，你可以采用以下方式，但仍应以“核心原创代码”为主：

1. 保留全部后端核心代码
2. 保留全部小程序页面逻辑代码
3. 适量保留页面样式代码
4. 不足页数时，让每个文件从新页开始排版，并保留空白，不要引入第三方依赖代码凑页数

不建议：

1. 加入 `.venv` 中的第三方库源码
2. 加入 `node_modules`
3. 加入构建后代码

## 8. 当前项目的推荐排版清单

下面是更适合实际打印的顺序：

1. `save_tears_backend/main.py`
2. `save_tears_backend/api.py`
3. `save_tears_miniprogram/src/main.ts`
4. `save_tears_miniprogram/src/App.vue`
5. `save_tears_miniprogram/src/api/index.ts`
6. `save_tears_miniprogram/src/pages/register/index.vue`
7. `save_tears_miniprogram/src/pages/login/index.vue`
8. `save_tears_miniprogram/src/pages/home/index.vue`
9. `save_tears_miniprogram/src/pages/profile/index.vue`
10. `save_tears_miniprogram/src/pages/admin/index.vue`
11. `save_tears_miniprogram/src/pages/water-flow/index.vue`
12. `save_tears_miniprogram/src/pages/sewage-turbidity/index.vue`
13. `save_tears_miniprogram/src/pages/water-bill/index.vue`
14. `save_tears_miniprogram/src/pages/index/index.vue`
15. `save_tears_miniprogram/src/uni.scss`
16. `save_tears_miniprogram/src/env.d.ts`
17. `save_tears_miniprogram/src/shime-uni.d.ts`
18. `save_tears_backend/test.py`

## 9. 文档材料配套建议

除源程序外，建议同步准备一份文档材料。这个项目可以使用：

- `softcopyright_materials/SOFTWARE_MANUAL.md`

按第十条规则，文档如果不足 60 页，也可以提交完整文档。你当前这份说明书草稿适合继续扩写并转成 Word/PDF。

## 10. 最终提交前检查表

1. 软件名称、版本号在页眉中保持一致
2. 源程序中的文件顺序已固定
3. 未混入第三方依赖代码
4. 未混入构建产物
5. 文档和程序均已转为 A4 排版
6. 著作权人名称和申请表保持一致
7. 若存在合作开发或委托开发，已准备权属证明

