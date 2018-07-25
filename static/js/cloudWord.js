/**
 * Created by hasee on 2017/10/17.
 */
var myChart = echarts.init(document.getElementById('main'));

var treeUrl = "https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=183389853,4064514913&fm=27&gp=0.jpg";

var presents = [
    '质量',
    '体积',
    '速度快',
    '读写',
    '外观',
    '配送及时',
    '外观',
    '漂亮',
    '超薄',
    '便携',
    '容量大','圣诞树', '贺卡', '圣诞礼盒', '围巾', '袜子', '苹果', '手链', '巧克力', '玫瑰', '香水', '乐高', '芭比', '项链'
];
var data = [];
for (var i = 0; i < presents.length; ++i) {
    data.push({
        name: presents[i],
        value: (presents.length - i) * 25
    });
}
for (var i = 10; i < presents.length; ++i) {
    var cnt = Math.floor(Math.random() * 15);
    console.log(cnt);
    for (var j = 0; j < cnt; ++j) {
        data.push({
            name: presents[i],
            value: Math.random() * 10
        });
    }
}


option = {
    tooltip: {
        show: false
    },
    series: [{
        type: 'wordCloud',
        gridSize: 2,
        sizeRange: [10, 35],
        rotationRange: [0, 90],
        rotationStep: 90,
        textStyle: {
            normal: {
                //颜色
                color: function (v) {
                    if (v.value > 600) {
                        return 'rgb(1, 25, 53)';
                    }
                    else if (v.value > 200) {
                        return 'rgb(0, 52, 63)';
                    }
                    else if (v.value > 9) {
                        return 'rgb(29, 176, 184)';
                    }
                    else {
                        return 'rgb(55, 198, 192)';
                    }
                }
            }
        },
        width: '80%',
        height: '80%',
        top: 40,
        data: data
    }],
    graphic: {
        elements: [{
            type: 'image',
            style: {
                width: 100,
                height: 100
            },
            left: 'center',
            top: 40
        }]
    }
};


var maskImage = new Image();
maskImage.onload = function () {
    console.log(maskImage);
    myChart.setOption({
        series: [{
            maskImage: maskImage
        }]
    });
};
maskImage.src = treeUrl;

myChart.setOption(option);