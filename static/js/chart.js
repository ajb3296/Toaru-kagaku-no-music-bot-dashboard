function set_chart(chart_list) {
    const chart_box = document.getElementsByClassName('chart')[0];
    let chart_item_html = "<table>"
    let count = 0;

    for (let i of chart_list) {
        count++;
        let chart_id = i[0];
        let chart_title = i[1];
        let chart_author = i[2];
        // let chart_count = i[3];
        chart_item_html += '' +
        '<tr class="chart_item">'+
        '    <td class="number">'+
        '        <a class="number_text">' + count + '</a>'+
        '    </td>'+
        '    <td class="music_author">'+
        '        <a href="https://www.youtube.com/watch?v=' + chart_id + '">' + chart_author + '</a>'+
        '    </td>'+
        '    <td class="music_title">'+
        '        <a href="https://www.youtube.com/watch?v=' + chart_id + '">' + chart_title + '</a>'+
        '    </td>'+
        '    <td class="image">'+
        '        <a href="https://www.youtube.com/watch?v=' + chart_id + '">'+
        '            <img src="http://img.youtube.com/vi/' + chart_id + '/0.jpg">'+
        '        </a>'+
        '    </td>'+
        '</tr>'
    }
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