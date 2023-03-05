function set_chart(chart_list) {
    const chart_box = document.getElementsByClassName('chart')[0];
    let chart_item_html = "";
    let count = 0;

    for (let i of chart_list) {
        count++;
        let chart_id = i[0];
        let chart_title = i[1];
        // let chart_count = i[2];
        chart_item_html += '<div class="chart_item">'+
        '    <div class="number">'+
        '        <a class="number_text">' + count + '</a>'+
        '    </div>'+
        '        <div class="music_title">'+
        '        <a>' + chart_title + '</a>'+
        '    </div>'+
        '    <div class="image">'+
        '        <img src="http://img.youtube.com/vi/' + chart_id + '/0.jpg">'+
        '    </div>'+
        '</div>'
    }
    console.log(chart_item_html)
    chart_box.innerHTML = chart_item_html;
}

function get_year(year) {
    $.ajax({
        url: '/statistics/year',
        type: 'POST',
        dataType: 'JSON',
        async: false,
        data: JSON.stringify({year: year}),
        contentType: "application/json",
        success: function(response) {
            result = response;
        },
        error: function(error) {
            console.log(error);
        }
    });
    if (result != null) {
        return result;
    }
    return false;
}