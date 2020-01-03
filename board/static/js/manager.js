// 自定义模块，这里只需要开放soulTable即可
layui.config({
    base: '/static/lib/layui_ext/',   // 模块所在目录
    version: 'v1.4.4' // 插件版本号
}).extend({
    soulTable: 'soulTable'  // 模块别名
});
var fileref = document.createElement('link');
fileref.setAttribute("rel", "stylesheet");
fileref.setAttribute("type", "text/css");
fileref.setAttribute("href", '/static/lib/layui_ext/css/soulTable.css');
document.getElementsByTagName("head")[0].appendChild(fileref);