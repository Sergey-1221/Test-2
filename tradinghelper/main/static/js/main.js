langRU = {
    time: {
        month: [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ],
        monthAbbr: [
            'Янв', 'Февр', 'Март', 'Апр', 'Май', 'Июнь',
            'Июль', 'Авг', 'Сент', 'Окт', 'Нояб', 'Дек'
        ],
        dayOfWeek: [
            'Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'
        ],
        dayOfWeekAbbr: [
            'вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'
        ]
    },
    legend: {
        selector: {
            all: 'Всё',
            inverse: 'Обратить'
        }
    },
    toolbox: {
        brush: {
            title: {
                rect: 'Выделить область',
                polygon: 'Инструмент «Лассо»',
                lineX: 'Горизонтальное выделение',
                lineY: 'Вертикальное выделение',
                keep: 'Оставить выбранное',
                clear: 'Очистить выбранное'
            }
        },
        dataView: {
            title: 'Данные',
            lang: ['Данные', 'Закрыть', 'Обновить']
        },
        dataZoom: {
            title: {
                zoom: 'Увеличить',
                back: 'Сбросить увеличение'
            }
        },
        magicType: {
            title: {
                line: 'Переключиться на линейный график',
                bar: 'Переключиться на столбчатую диаграмму',
                stack: 'Стопка',
                tiled: 'Плитка'
            }
        },
        restore: {
            title: 'Восстановить'
        },
        saveAsImage: {
            title: 'Сохранить картинку',
            lang: ['Правый клик, чтобы сохранить картинку']
        }
    },
    series: {
        typeNames: {
            pie: 'Круговая диаграмма',
            bar: 'Столбчатая диаграмма',
            line: 'Линейный график',
            scatter: 'Точечная диаграмма',
            effectScatter: 'Точечная диаграмма с волнами',
            radar: 'Лепестковая диаграмма',
            tree: 'Дерево',
            treemap: 'Плоское дерево',
            boxplot: 'Ящик с усами',
            candlestick: 'Свечной график',
            k: 'График К-линий',
            heatmap: 'Тепловая карта',
            map: 'Карта',
            parallel: 'Диаграмма параллельных координат',
            lines: 'Линейный граф',
            graph: 'Граф отношений',
            sankey: 'Диаграмма Санкей',
            funnel: 'Воронкообразная диаграмма',
            gauge: 'Шкала',
            pictorialBar: 'Столбец-картинка',
            themeRiver: 'Тематическая река',
            sunburst: 'Солнечные лучи'
        }
    },
    aria: {
        general: {
            withTitle: 'Это график, показывающий "{title}"',
            withoutTitle: 'Это график'
        },
        series: {
            single: {
                prefix: '',
                withName: ' с типом {seriesType} и именем {seriesName}.',
                withoutName: ' с типом {seriesType}.'
            },
            multiple: {
                prefix: '. Он состоит из {seriesCount} серий.',
                withName:
                    ' Серия {seriesId} имеет тип {seriesType} и показывает {seriesName}.',
                withoutName: ' Серия {seriesId} имеет тип {seriesType}.',
                separator: {
                    middle: '',
                    end: ''
                }
            }
        },
        data: {
            allData: 'Данные таковы: ',
            partialData: 'Первые {displayCnt} элементов: ',
            withName: 'значение для {name} — {value}',
            withoutName: '{value}',
            separator: {
                middle: ', ',
                end: '. '
            }
        }
    }
};