let year_data = get_year(2023)

if (year_data !== false) {
    for (let i of year_data) {
        console.log(i);
    }
}

set_chart(year_data);