var cmdInfoTpl = "\
    <h3>{{ d.cmdno }}</h3>\
    <h3>{{ d.name }}</h3>\
    <h3>{{ d.ch_name }}</h3>\
    <h3>{{ d.gtp }}</h3>\
    <ul>\
        {{# layui.each(d.fields, function(index, item){ }}\
        <li>\
            <span>字段名称：</span>\
            <span>{{ item.f_name }}</span>\
        </li>\
        <li>\
            <span>字段类型：</span>\
            <span>{{ item.f_type.t_type }}</span>\
        </li>\
        <li>\
            <span>字段属性：</span>\
            <span>{{ item.f_type.t_group }}</span>\
        </li>\
        <li>\
            <span>字段长度：</span>\
            <span>{{ item.f_type.t_length }}</span>\
        </li>\
        <li>\
            <span>00000：</span>\
            <span>{{ item.site || '' }}</span>\
        </li>\
        {{# }); }}\
        {{# if(d.fields.length === 0){ }}\
        无数据\
        {{# } }}\
    </ul>\
   ";
layui.use(['jquery', 'laytpl'], function () {
    var $ = layui.$;
    var laytpl = layui.laytpl;
    $.get("{{ url('api_cmd',project=cmd_prj,application=cmd_app,name=cmd_name) }}", function (result) {
        var data = result.data;
        var getTpl = cmdInfoTpl.innerHTML, view = document.getElementById('view');
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    });
});
layui.use('laydate', function () {
    var laydate = layui.laydate;

    //执行一个laydate实例
    laydate.render({
        elem: '#start' //指定元素
    });

    //执行一个laydate实例
    laydate.render({
        elem: '#end' //指定元素
    });

});
layui.use('table', function () {
    var table = layui.table;

    //监听单元格编辑
    table.on('edit(test)', function (obj) {
        var value = obj.value //得到修改后的值
            ,
            data = obj.data //得到所在行所有键值
            ,
            field = obj.field; //得到字段
        layer.msg('[ID: ' + data.id + '] ' + field + ' 字段更改为：' + value);
    });

    //头工具栏事件
    table.on('toolbar(test)', function (obj) {
        var checkStatus = table.checkStatus(obj.config.id);
        switch (obj.event) {
            case 'getCheckData':
                var data = checkStatus.data;
                layer.alert(JSON.stringify(data));
                break;
            case 'getCheckLength':
                var data = checkStatus.data;
                layer.msg('选中了：' + data.length + ' 个');
                break;
            case 'isAll':
                layer.msg(checkStatus.isAll ? '全选' : '未全选');
                break;
        }
    });

    //监听排序事件
    table.on('sort(test)', function (obj) { //注：sort 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
        //尽管我们的 table 自带排序功能，但并没有请求服务端。
        //有些时候，你可能需要根据当前排序的字段，重新向服务端发送请求，从而实现服务端排序，如：
        table.reload('test', {
            initSort: obj //记录初始排序，如果不设的话，将无法标记表头的排序状态。
            , where: { //请求参数（注意：这里面的参数可任意定义，并非下面固定的格式）
                field: obj.field //排序字段
                , order: obj.type //排序方式
            }
        });
        //layer.msg('服务端排序。order by ' + obj.field + ' ' + obj.type);
    });
});