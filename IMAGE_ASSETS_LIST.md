# 图片资源位置清单

以下是小程序项目中所有引用图片资源 (`/static/images/...`) 的代码位置。
我已经直接在 `.vue` 文件的代码中添加了 `<!-- TODO: ... -->` 注释，您可以直接在代码编辑器中搜索 "TODO" 来快速定位。

## 1. 登录页 (`save_tears_miniprogram/src/pages/login/index.vue`)
- **Line 6**: 背景图片 (`bg_login.jpg`)
    - 搜索注释: `<!-- TODO: Replace background image here -->`
- **Line 16**: 圆形 Logo 头像 (`logo_avatar.jpg`)
    - 搜索注释: `<!-- TODO: Replace logo avatar here -->`

## 2. 注册页 (`save_tears_miniprogram/src/pages/register/index.vue`)
- **Line 4**: 背景图片 (`bg_login.jpg`)
    - 搜索注释: `<!-- TODO: Replace background image here -->`
- **Line 10**: 圆形 Logo 头像 (`logo_avatar.jpg`)
    - 搜索注释: `<!-- TODO: Replace logo avatar here -->`

## 3. 首页 (`save_tears_miniprogram/src/pages/home/index.vue`)
- **Line 4**: 背景图片 (`bg_login.jpg`)
    - 搜索注释: `<!-- TODO: Replace background image here -->`
- **Line 12**: 顶部小头像 (`logo_avatar.jpg`)
    - 搜索注释: `<!-- TODO: Replace small avatar here -->`

## 4. 个人中心页 (`save_tears_miniprogram/src/pages/profile/index.vue`)
- **Line 9**: 用户头像 (`logo_avatar.jpg`)
    - 搜索注释: `<!-- TODO: Replace user avatar here -->`

## 5. 管理员页 (`save_tears_miniprogram/src/pages/admin/index.vue`)
- **Line 4**: 管理员背景图 (`bg_admin.jpg`)
    - 搜索注释: `<!-- TODO: Replace admin background here -->`

## 6. 全局配置 (`save_tears_miniprogram/src/pages.json`)
*(注意：此文件是 JSON 配置，无法直接添加注释，请直接参照行号修改)*
- **Line 55**: 首页 Tab 图标 (`tab_home.png`)
- **Line 56**: 首页选中态 Tab 图标 (`tab_home_active.png`)
- **Line 61**: 我的 Tab 图标 (`tab_profile.png`)
- **Line 62**: 我的选中态 Tab 图标 (`tab_profile_active.png`)

---
**提示**：
您可以将新的图片放入 `src/static/images/` 文件夹中，然后修改上述代码中的文件名即可生效。
