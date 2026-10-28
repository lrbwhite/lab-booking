# uvicorn 事件循环

python 异步编程，前端fetch，axios，现在实现的流式效果

# 流式内容先空白最后一次性，冒出内容

AIChat.vue L94

先前的reply不是响应式对象，**没有被 Proxy 包住,** **原始对象的属性绕过了 Proxy 的 `set` 拦截器。**使得每次更改后会出现空白

`ref`/`reactive` 只对**经过 Proxy 的读写**生效；对象一旦以原始引用被外部持有，改它等于改“影子”，界面不会更新。
