// JavaScript Document

/* jshint esversion: 6 */

let result_ajax_detail = {};
let paper_page_total = 0;
let paper_page_current = 0;

// 查询专家详情
function query_detail_ajax(expert_id) {
	'use strict';

	let startDate = new Date();
	let endDate;

	let server_url = "detail";

	let post_data = {};
	if(!expert_id || expert_id === "") {
		return false;
	} else {
		post_data.id = expert_id;
	}

	// HTTP GET (JQuery Ajax)
	$.ajax({
		type: "GET",
		url: server_url,
		data: post_data,
		dataType: "json",
		beforeSend: function(xhr) {
			endDate = new Date();
			console.log("初始耗时：", endDate - startDate);

			console.log("$.ajax beforeSend, state = " + xhr.status);
			// 出现loading动画
			$('#intro .load-container').css({"display": "block"});
		},
		success: function(result, status, xhr) {
			endDate = new Date();
			console.log("初始耗时 + AJAX耗时：", endDate - startDate);

			console.log("$.ajax success, state = " + xhr.status);
			// 隐藏loading动画
			$('#intro .load-container').css({"display": "none"});

			if(!result || result === "" || result.length === 0) {
				// TODO
			    $.toast({
					text: "抱歉，该专家无信息！",
					showHideTransition: 'plain',
					bgColor: 'red',
					textColor: '#e0e0e0',
					allowToastClose : false,
					hideAfter: 2400,
					stack: 5,
					textAlign: 'center',
					position: 'mid-center'
				});
				console.log("抱歉，该专家无信息。");
				return false;
			}

			// 解析JSON数据
			result_ajax_detail.expert_basic = JSON.parse(result.expert_basic);
			result_ajax_detail.expert_academic = JSON.parse(result.expert_academic);
			result_ajax_detail.papers = JSON.parse(result.papers);
			result_ajax_detail.co_experts_info = JSON.parse(result.co_experts_info);
			result_ajax_detail.influ_info = JSON.parse(result.influ_info);

			paper_page_total = Math.floor(result_ajax_detail.papers.length / 10) + 1;
			paper_page_current = 1;
			// 使paper_page_current和paper_page_total为十进制整数
			paper_page_total = parseInt(paper_page_total, 10);
			paper_page_current = parseInt(paper_page_current, 10);

			console.log(result_ajax_detail);
			console.log(JSON.parse(result_ajax_detail.papers[0]));

			// 使用数据渲染页面
			result = result_ajax_detail;
            render_detail_page(result);

            endDate = new Date();
			console.log("初始耗时 + AJAX耗时 + 渲染耗时：", endDate - startDate);

			return true;
		},
		error: function(xhr, status, error) {
			console.log("$.ajax error, state = " + xhr.status);
			// 隐藏loading动画
			$('#intro .load-container').css({"display": "none"});
			alert('HTTP GET Error! status=' + status + '&error=' + error +
				'&statusCode=' + xhr.status + '&responseText=' + xhr.responseText +
				 '&readyState=' + xhr.readyState);
		},
		statusCode: {
			// 当响应对应的状态码时，执行对应的回调函数
			200: function() {
				console.log("200: 请求成功");
			},
			404: function() {
				console.log("404: 找不到页面");
				alert("404: 找不到页面");
			},
			500: function() {
				console.log("500: 服务器错误");
				alert( "500: 服务器错误" );
			}
		},
	});
}


// 渲染详情页
function render_detail_page(result_ajax) {
    'use strict';

    // 绘制影响力变化曲线图
	drawInfluenceEcharts(result_ajax);

    // 绘制专家关系图
    relationshipNet(result_ajax);

    // 增添其它信息
    let jq_researcher_academic_content = $('#researcher_academic_content > table > tbody > tr:first-child');
    let jq_this_researcher_name = $('.this_researcher_name');
    let jq_this_researcher_university = $('.this_researcher_university');
    let jq_this_researcher_college = $('.this_researcher_college');
    let jq_this_researcher_subject = $('#researcher_academic_content .this_researcher_subject');
    let jq_this_researcher_theme = $('#researcher_academic_content .this_researcher_theme');
    let jq_this_researcher_papers = $('#researcher_papers ul.papers');
    let jq_this_researcher_image = $('img.researcher_image');
    let jq_this_researcher_resume = $('#researcher_resume article.resume');
    let jq_current_page = $('#current_page');
    let jq_total_pages = $('#total_pages');
    let jq_paper_previous_page = $('#paper_previous_page');
    let jq_paper_next_page = $('#paper_next_page');

    let html_template;
    html_template = '<td>' + result_ajax.expert_academic.amount1 + '</td>' +
		'<td>' + (result_ajax.expert_academic.amount2 || '无数据') + '</td>' +
		'<td>' + (result_ajax.expert_academic.h_index || '无数据') + '</td>' +
		'<td>' + (result_ajax.expert_academic.core || '无数据') + '</td>' +
		'<td>' + (result_ajax.expert_academic.cssci || '无数据') + '</td>' +
		'<td>' + (result_ajax.expert_academic.rdfybkzl || '无数据') + '</td>';
    jq_researcher_academic_content.empty();
    jq_researcher_academic_content.append(html_template);

    jq_this_researcher_name.empty();
    jq_this_researcher_name.append(result_ajax.expert_academic.name || '无姓名');

    jq_this_researcher_university.empty();
    jq_this_researcher_university.append(result_ajax.expert_basic.university || '无所属学校信息');

    jq_this_researcher_college.empty();
    jq_this_researcher_college.append(result_ajax.expert_basic.college || '无所属学院信息');

    jq_this_researcher_subject.empty();
    jq_this_researcher_subject.append(result_ajax.expert_basic.sub_list || '无所属学院信息');

    jq_this_researcher_theme.empty();
    jq_this_researcher_theme.append(result_ajax.expert_basic.theme_list || '无所属学院信息');

    jq_current_page.empty();
    jq_current_page.append(paper_page_current);

    jq_total_pages.empty();
    jq_total_pages.append(paper_page_total);

    // 使上一页按钮不可选
	if(!jq_paper_previous_page.hasClass("disabled")) {
    	jq_paper_previous_page.addClass("disabled");
	}

    // 若总共仅一页,则使下一页按钮也不可选
    if(paper_page_total === 1 && !jq_paper_next_page.hasClass("disabled")) {
    	jq_paper_next_page.addClass("disabled");
	}

    // 若数据库中有学者的头像,则将页面中的默认头像更换掉
	let expert_image = result_ajax.expert_basic.img_url;
	if(expert_image && expert_image !== '') {
		jq_this_researcher_image.attr({"src": expert_image});
	}

	// 学者简历信息
	let expert_resume = result_ajax.expert_basic.resume;
	if(expert_resume && expert_resume !== '') {
		jq_this_researcher_resume.append('<p>' + expert_resume + '</p>');
	} else {
		jq_this_researcher_resume.append('<p>无该学者简历数据.</p>');
	}

    // 展示前10篇论文(每页10篇,页码从1开始)
	let paper_item;
    html_template = '';
    let first_page_papers = result_ajax.papers.slice(0, 10);
    first_page_papers.forEach(function (item, index) {
    	// 解析数据为JSON格式
    	paper_item = JSON.parse(item);

    	// 取authors字段的前五名作者
    	let paper_authors_name = paper_item.authors.split(' ').slice(0, 5);

    	// 获取作者id信息(在数据库中存在的作者才有id,否则只有名字)
		let paper_authors_id = [];
		if(paper_item.author1 && (paper_item.author1 !== '')) {
			paper_authors_id.push(paper_item.author1);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author2 && (paper_item.author2 !== '')) {
			paper_authors_id.push(paper_item.author2);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author3 && (paper_item.author3 !== '')) {
			paper_authors_id.push(paper_item.author3);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author4 && (paper_item.author4 !== '')) {
			paper_authors_id.push(paper_item.author4);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author5 && (paper_item.author5 !== '')) {
			paper_authors_id.push(paper_item.author5);
		} else {
			paper_authors_id.push('');
		}

		// 设置html结点
    	html_template += '<li><article><header><h3><a>' + paper_item.title + '</a></h3></header>';

		// 设置作者
		html_template += '<p>';
		let i;
		for(i = 0 ; i < paper_authors_name.length ; i++) {
			if(paper_authors_id[i] === '') {
				// 若作者无id,表示该作者不在数据库中,故不做链接跳转
				html_template += (paper_authors_name[i] || paper_authors_id[i]) + ' , ';
			} else {
				html_template += '<a onclick="jumpToAnotherResearcher(' + paper_authors_id[i] + ')">' +
					(paper_authors_name[i] || paper_authors_id[i]) + '</a>' + ' , ';
			}
		}
		// 截去字符串最后的' , '
		html_template = html_template.substring(0, (html_template.length - 3));

		// 设置其它论文信息
		html_template += ' | ' + (paper_item.type || '') + ' | ' + paper_item.source + '</p>';

		html_template += '<p><strong>' + '摘要</strong>: ' + paper_item.abstract + '</p>';

		html_template += '<p><strong>' + '关键字</strong>: ' + paper_item.keyword + '</p>';

		html_template += '</article></li>';
    });
    jq_this_researcher_papers.empty();
    jq_this_researcher_papers.append(html_template);
}


// 分页展示论文-上一页
function previousPaperPage() {
	'use strict';
	let jq_current_page = $('#current_page');
    let jq_paper_previous_page = $('#paper_previous_page');
    let jq_paper_next_page = $('#paper_next_page');

	if(!paper_page_current || paper_page_current <= 0 || paper_page_current > paper_page_total) {
		console.log('pre_page_error! paper_page_current is out of range.');
		return false;
	} else if(paper_page_current === 1) {
		$.toast({
			text: "当前页已经是第一页了！",
			showHideTransition: 'plain',
			bgColor: 'orange',
			textColor: '#e0e0e0',
			allowToastClose : false,
			hideAfter: 1500,
			stack: 5,
			textAlign: 'center',
			position: 'mid-center'
		});
		return false;
	} else {
		paper_page_current --;

		jq_current_page.empty();
		jq_current_page.append(paper_page_current);

		// 若按上一页之后到了第一页,则使上一页按钮不可选
		if(paper_page_current === 1 && !jq_paper_previous_page.hasClass("disabled")) {
			jq_paper_previous_page.addClass("disabled");
		}

		// 若下一页按钮之前有disabled属性,则撤销之
		if(jq_paper_next_page.hasClass("disabled")) {
			jq_paper_next_page.removeClass("disabled");
		}

		// 改变页面中的论文内容
		change_paper_page();
	}
	return true;
}


// 分页展示论文-下一页
function nextPaperPage() {
	'use strict';
	let jq_current_page = $('#current_page');
	let jq_paper_previous_page = $('#paper_previous_page');
	let jq_paper_next_page = $('#paper_next_page');

	if(!paper_page_current || paper_page_current <= 0 || paper_page_current > paper_page_total) {
		console.log('next_page_error! paper_page_current is out of range.');
		return false;
	} else if(paper_page_current === paper_page_total) {
		$.toast({
			text: "当前页已经是最后一页了！",
			showHideTransition: 'plain',
			bgColor: 'orange',
			textColor: '#e0e0e0',
			allowToastClose : false,
			hideAfter: 1500,
			stack: 5,
			textAlign: 'center',
			position: 'mid-center'
		});
		return false;
	} else {
		paper_page_current ++;

		jq_current_page.empty();
		jq_current_page.append(paper_page_current);

		// 若按下一页之后到了最后一页,则使下一页按钮不可选
		if(paper_page_current === paper_page_total && !jq_paper_next_page.hasClass("disabled")) {
			jq_paper_next_page.addClass("disabled");
		}

		// 若上一页按钮之前有disabled属性,则撤销之
		if(jq_paper_previous_page.hasClass("disabled")) {
			jq_paper_previous_page.removeClass("disabled");
		}

		// 改变页面中的论文内容
		change_paper_page();
	}
	return true;
}


// 分页展示论文-按页码跳转
function jumpPaperPage() {
	'use strict';
	let jq_current_page = $('#current_page');
	let jq_paper_previous_page = $('#paper_previous_page');
	let jq_paper_next_page = $('#paper_next_page');
	let page_input = Math.floor( parseInt($('#paper_jump_input').val().toString().trim(), 10) );

	if(!paper_page_current || paper_page_current <= 0 || paper_page_current > paper_page_total) {
		console.log('input_jump_page_error! paper_page_current is out of range.');
		return false;
	} else if(!page_input || page_input === "") {
		$.toast({
			text: "请输入合法页码！",
			showHideTransition: 'plain',
			bgColor: 'orange',
			textColor: '#e0e0e0',
			allowToastClose : false,
			hideAfter: 1500,
			stack: 5,
			textAlign: 'center',
			position: 'mid-center'
		});
		return false;
	} else if(parseInt(page_input, 10) <= 0 || parseInt(page_input, 10) > paper_page_total) {
		$.toast({
			text: "论文信息总共" + paper_page_total + "页，请输入该范围内的页码！",
			showHideTransition: 'plain',
			bgColor: 'orange',
			textColor: '#e0e0e0',
			allowToastClose : false,
			hideAfter: 1500,
			stack: 5,
			textAlign: 'center',
			position: 'mid-center'
		});
		return false;
	} else {
		paper_page_current = parseInt(page_input, 10);

		jq_current_page.empty();
		jq_current_page.append(paper_page_current);

		// 若跳转到了第一页,则使上一页按钮不可选
		if(paper_page_current === 1 && !jq_paper_previous_page.hasClass("disabled")) {
			jq_paper_previous_page.addClass("disabled");
		}

		// 若跳转到了最后一页,则使下一页按钮不可选
		if(paper_page_current === paper_page_total && !jq_paper_next_page.hasClass("disabled")) {
			jq_paper_next_page.addClass("disabled");
		}

		// 若跳转到了中间页码,使上一页和下一页按钮都可选
		if(paper_page_current > 1 && paper_page_current < paper_page_total) {
			if(jq_paper_previous_page.hasClass("disabled")) {
				jq_paper_previous_page.removeClass("disabled");
			}
			if(jq_paper_next_page.hasClass("disabled")) {
				jq_paper_next_page.removeClass("disabled");
			}
		}

		// 改变页面中的论文内容
		change_paper_page();
	}

	return true;
}


// 换页时，改变查询结果内容
function change_paper_page() {
	'use strict';

	if(!result_ajax_detail || result_ajax_detail.length === 0 || result_ajax_detail === "" ||
		paper_page_current <= 0 || paper_page_total <= 0 ||
		paper_page_current > paper_page_total ) {
		console.log('function change_paper_page() error: global variables error.');
		return false;
	}
	
	let result = result_ajax_detail;
	let result_total_page = paper_page_total;
	let result_now_page = paper_page_current;

	let jq_this_researcher_papers = $('#researcher_papers ul.papers');
	let jq_paper_jump_input = $('#paper_jump_input');

	let paper_item;
    let html_template = '';
    let this_page_papers = result.papers.slice((paper_page_current - 1) * 10, paper_page_current * 10);
    this_page_papers.forEach(function (item, index) {
    	// 解析数据为JSON格式
    	paper_item = JSON.parse(item);

    	// 取authors字段的前五名作者
    	let paper_authors_name = paper_item.authors.split(' ').slice(0, 5);

    	// 获取作者id信息(在数据库中存在的作者才有id,否则只有名字)
		let paper_authors_id = [];
		if(paper_item.author1 && (paper_item.author1 !== '')) {
			paper_authors_id.push(paper_item.author1);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author2 && (paper_item.author2 !== '')) {
			paper_authors_id.push(paper_item.author2);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author3 && (paper_item.author3 !== '')) {
			paper_authors_id.push(paper_item.author3);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author4 && (paper_item.author4 !== '')) {
			paper_authors_id.push(paper_item.author4);
		} else {
			paper_authors_id.push('');
		}
		if(paper_item.author5 && (paper_item.author5 !== '')) {
			paper_authors_id.push(paper_item.author5);
		} else {
			paper_authors_id.push('');
		}

		// 设置html结点
    	html_template += '<li><article><header><h3><a>' + paper_item.title + '</a></h3></header>';

		// 设置作者
		html_template += '<p>';
		let i;
		for(i = 0 ; i < paper_authors_name.length ; i++) {
			if(paper_authors_id[i] === '') {
				// 若作者无id,表示该作者不在数据库中,故不做链接跳转
				html_template += (paper_authors_name[i] || paper_authors_id[i]) + ' , ';
			} else {
				html_template += '<a onclick="jumpToAnotherResearcher(' + paper_authors_id[i] + ')">' +
					(paper_authors_name[i] || paper_authors_id[i]) + '</a>' + ' , ';
			}
		}
		// 截去字符串最后的' , '
		html_template = html_template.substring(0, (html_template.length - 3));

		// 设置其它论文信息
		html_template += ' | ' + (paper_item.type || '') + ' | ' + paper_item.source + '</p>';

		html_template += '<p><strong>' + '摘要</strong>: ' + paper_item.abstract + '</p>';

		html_template += '<p><strong>' + '关键字</strong>: ' + paper_item.keyword + '</p>';

		html_template += '</article></li>';
    });
    jq_this_researcher_papers.empty();
    jq_this_researcher_papers.append(html_template);

    // 清空页码输入框
    jq_paper_jump_input.val("");
}


// 跳转到另一个学者详情页
function jumpToAnotherResearcher(expert_id) {
	'use strict';
	// 如果不是本页学者，则跳转
	if(expert_id.toString() !== result_ajax_detail.expert_basic.id) {
		window.location.href = "detail?id=" + expert_id;
		return true;
	} else {
		return false;
	}
}


// TODO 详情页内的查询
function searchAnotherResearcher() {
	'use strict';
	let query_input = $("input[name='query_another']").val().trim();
	console.log(query_input);
	return true;
}


// 平滑移动到锚点
function scrollAnchor(anchor_id) {
	$('html, body').animate({
		// 该div容器的padding-top是3em
		scrollTop: $('#' + anchor_id).offset().top - 3 * 16
	}, 600);
	// document.getElementById(anchor_id).scrollIntoView();
}


// 绘制专家关系图 TODO 调整初始图像美观度;增添文字描述;增添链接跳转;分类显示合作学者/合作机构.
function relationshipNet(result_ajax) {
	// 获取所有相关专家数据
	let co_expert_array = [];
	result_ajax.co_experts_info.forEach(function (item, index) {
		co_expert_array.push(JSON.parse(item));
    });
	console.log(co_expert_array);

	// 获取所有合作学者的年份
	// jq_relationship_year = $('select#relationship_year');
	// let year_list = [];	// 相关专家的年份列表
	// co_expert_array.forEach(function (item, index) {
	// 	if(year_list.length === 0) {
	// 		year_list.push(item.co_year);
	// 	} else {
	// 		if(year_list.indexOf(item.co_year) === -1) {
	// 			year_list.push(item.co_year);
	// 		}
	// 	}
	// });
	// year_list = year_list.sort().reverse();
    //
	// // select 增加 option
	// let year_option_html = '';
	// year_list.forEach(function (item, index) {
	// 	year_option_html += '<option value="' + item + '">' + item + '</option>';
    // });
	// jq_relationship_year.empty();
	// jq_relationship_year.append(year_option_html);

	// 绘力导向图
	drawNetworkEcharts(co_expert_array);

	// TODO 关系网络分析

	// TODO 点击相关学者进行跳转

	// TODO 用按钮控制 show or hide 图中的结点
}


// 绘制 Echarts 影响力变化曲线图
function drawInfluenceEcharts(result_ajax) {
	// 设置容器的宽高
	let jq_influence_canvas_div = $('#researcher_influence_div');
	let jq_influence_echarts = $('div#influence_echarts');

	let width = jq_influence_canvas_div.width();
	let height = window.innerHeight / 2;
	jq_influence_echarts.width(width);
	jq_influence_echarts.height(height);

	// 给容器增加边框
	jq_influence_canvas_div.css({"border": "1px solid #aaa"});

	// 基于准备好的 dom，初始化 echarts 实例
	let myChart = echarts.init(document.getElementById('influence_echarts'));

	// 规整化影响力值
	let influ_info = result_ajax.influ_info;
	if(influ_info.influ_19 === -1) {
		influ_info.influ_19 = 0;
	}
	if(influ_info.influ_1990 === -1) {
		influ_info.influ_1990 = influ_info.influ_19;
	}
	if(influ_info.influ_1995 === -1) {
		influ_info.influ_1995 = influ_info.influ_1990;
	}
	if(influ_info.influ_2000 === -1) {
		influ_info.influ_2000 = influ_info.influ_1995;
	}
	if(influ_info.influ_2005 === -1) {
		influ_info.influ_2005 = influ_info.influ_2000;
	}
	if(influ_info.influ_2010 === -1) {
		influ_info.influ_2010 = influ_info.influ_2005;
	}
	if(influ_info.influ_2015 === -1) {
		influ_info.influ_2015 = influ_info.influ_2010;
	}
	console.log(influ_info);

	// 指定图表的配置项和数据
	let option = {
		xAxis: {
			type: 'category',
			data: ['1990以前', '1990~1995', '1995~2000', '2000~2005', '2005~2010', '2010~2015', '2015至今']
		},
		yAxis: {
			type: 'value'
		},
		tooltip: {
			trigger: 'axis'
		},
		series: [{
			data: [influ_info.influ_19, influ_info.influ_1990, influ_info.influ_1995, influ_info.influ_2000,
				influ_info.influ_2005, influ_info.influ_2010, influ_info.influ_2015],
			type: 'line',
			legendHoverLink: true,	// 是否启用图例 hover(悬停) 时的联动高亮
			hoverAnimation: true,	// 是否开启鼠标悬停节点的显示动画
			smooth: true
		}]
	};

	/*
	let option = {
		legend: {
			// 图例位置
			x: 'left',
			// 设置初始只显示相关机构和最近一年的合作学者
			selected: un_show_legend_list,
			// 图例的名称，必须和关系网类别中 name 相对应
			data: network_info.categories.map(function (item) {
				return item.name;
			})
		},
		series: [{
			type: 'graph',		// 关系图
			// name: "合作关系",		// 系列名称，用于tooltip的显示，legend 的图例筛选，在 setOption 更新数据和配置项时用于指定对应的系列
			layout: 'force',	// 图的布局，类型为力导图，'circular' 采用环形布局
			legendHoverLink: true,	// 是否启用图例 hover(悬停) 时的联动高亮
			hoverAnimation: true,	// 是否开启鼠标悬停节点的显示动画
			coordinateSystem: null,	// 坐标系可选
			xAxisIndex: 0, 		// x轴坐标 有多种坐标系轴坐标选项
			yAxisIndex: 0,		// y轴坐标
			roam: false,		// 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
			nodeScaleRatio: 0,	// 鼠标漫游缩放时节点的相应缩放比例，当设为0时节点不随着鼠标的缩放而缩放
			draggable: true,	// 节点是否可拖拽，只在使用力引导布局的时候有用。
			focusNodeAdjacency: true,	// 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。
			// animation: false,
			label: {
				normal: {
					show: true,
					position: 'right'
				}
			},
			force: {
				layoutAnimation: true,
				// xAxisIndex : 0,	// x轴坐标, 有多种坐标系轴坐标选项
				// yAxisIndex : 0,	// y轴坐标
				gravity: 0.03,		//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
				edgeLength: 70,		//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
				repulsion: 150		//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
			},
			// node数据
			data: network_info.nodes.map(function (node, index) {
				node.id = index;
				return node;
			}),
			// 关系网类别，可以写多组
			categories: network_info.categories,
			// link数据
			edges: network_info.links,
			// 边两端的标记类型，可以是一个数组分别指定两端，也可以是单个统一指定。默认不显示标记，常见的可以设置为箭头，
			// 如：edgeSymbol: ['circle', 'arrow']
			edgeSymbol: ['none', 'none'],
			edgeSymbolSize: 10	// 边两端的标记大小，可以是一个数组分别指定两端，也可以是单个统一指定。

			// symbol:'roundRect',	// 关系图节点标记的图形。ECharts 提供的标记类型包括 'circle'(圆形), 'rect'（矩形）,
			// 'roundRect'（圆角矩形）, 'triangle'（三角形）, 'diamond'（菱形）, 'pin'（大头针）, 'arrow'（箭头）.
			// 也可以通过 'image://url' 设置为图片，其中 url 为图片的链接。'path:// 这种方式可以任意改变颜色并且抗锯齿

			// symbolSize:10 ,		// 也可以用数组分开表示宽和高，例如 [20, 10] 如果需要每个数据的图形大小不一样，可以设置为如下格式的回调函数：(value: Array|number, params: Object) => number|Array
			// symbolRotate:,		// 关系图节点标记的旋转角度。注意在 markLine 中当 symbol 为 'arrow' 时会忽略 symbolRotate 强制设置为切线的角度。
			// symbolOffset:[0,0],	// 关系图节点标记相对于原本位置的偏移。[0, '50%']
		}],
		tooltip: {
			show: true,	// 默认显示
			showContent :true,	// 是否显示提示框浮层
			trigger: 'item',	// 触发类型，默认数据项触发
			triggerOn: 'click',	// 提示触发条件，mousemove鼠标移至触发，还有click点击触发
			alwaysShowContent: false,	// 默认离开提示框区域隐藏，true为一直显示
			showDelay: 0,		// 浮层显示的延迟，单位为 ms，默认没有延迟，也不建议设置。在 triggerOn 为 'mousemove' 时有效。
			hideDelay: 200,		// 浮层隐藏的延迟，单位为 ms，在 alwaysShowContent 为 true 的时候无效。
			enterable: false,	// TODO 鼠标是否可进入提示框浮层中，默认为false，如需详情内交互，如添加链接、按钮，可设置为 true。
			position: 'right',	// 提示框浮层的位置，默认不设置时位置会跟随鼠标的位置。只在 trigger 为'item'的时候有效。
			confine: false,		//是否将 tooltip 框限制在图表的区域内。外层的 dom 被设置为 'overflow: hidden'，或者移动端窄屏，
			// 导致 tooltip 超出外界被截断时，此配置比较有用。
			transitionDuration: 0.4,	// 提示框浮层的移动动画过渡时间，单位是 s，设置为 0 的时候会紧跟着鼠标移动。
		}
	};
	*/

	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(option);
}


// 绘制 Echarts 关系图
function drawNetworkEcharts(co_expert_array) {
	result_ajax = result_ajax_detail;

	// 设置容器的宽高
	let jq_relationship_canvas_div = $('#relationship_picture_div');
	let jq_relationship_echarts = $('div#relationship_echarts');

	let width = jq_relationship_canvas_div.width();
	let height = window.innerHeight / 8 * 5;
	jq_relationship_echarts.width(width);
	jq_relationship_echarts.height(height);

	// 给容器增加边框
	jq_relationship_canvas_div.css({"border": "1px solid #aaa"});

	let co_agency_string = result_ajax.expert_academic.co_agency;
	co_agency_string = co_agency_string.replace(/\[/g, '');
	co_agency_string = co_agency_string.replace(/]/g, '');
	co_agency_string = co_agency_string.replace(/'/g, '');
	co_agency_string = co_agency_string.replace(/ /g, '');

	let co_agency_list = co_agency_string.split(',');

	let network_info = {
		// 关系网类别
		categories: [
			{name: result_ajax.expert_basic.name},
			],
		// 节点
		// category 与关系网类别索引对应，id 是自动生成的
		nodes: [
			{category: 0, name: result_ajax.expert_basic.name, value: 5, id: 0},
			],
		// 节点之间连线
		// source起始节点，0表示第一个节点
		// target目标节点，1表示与索引(id)为1的节点进行连接
		links: []
	};

	// 把相关机构的 node link 信息写入关系网
	let node_id = 1;
	let category_id = 1;
	network_info.categories.push({name: "相关机构"});
	co_agency_list.forEach(function (item, index) {
		network_info.nodes.push({
			category: category_id,
			name: item,
			value: 3,	// TODO 节点 value
			id: node_id
		});
		network_info.links.push({
			source: node_id,
			target: 0,	// 连线目标都是 0
			value: 3	// TODO 连线 value 随关系强度变化
		});
		node_id ++;
    });
	category_id ++;

	// console.log(network_info);

	// 获取所有合作学者的年份
	let year_list = [];	// 相关专家的年份列表
	co_expert_array.forEach(function (item, index) {
		if(year_list.length === 0) {
			year_list.push(item.co_year);
		} else {
			if(year_list.indexOf(item.co_year) === -1) {
				year_list.push(item.co_year);
			}
		}
	});
	year_list = year_list.sort().reverse();

	// 获取当前所选的年份
	// let relationship_year = ''
	// jq_relationship_year = $('select#relationship_year');
	// relationship_year = jq_relationship_year.val()

	// 初始状态选择最近的一年的论文合作学者
	// jq_relationship_type = $('select#relationship_type option:selected');
	// relationship_type = jq_relationship_type.val();

	// 每一年一个类，写入关系网
	let flag = true;
	year_list.forEach(function (this_year, index) {
		flag = true;
		co_expert_array.forEach(function (co_expert, index) {
			if(co_expert.co_year === this_year) {
				if(flag) {
					network_info.categories.push({name: this_year + "年 论文合作学者"});
					flag = false;
				}
				network_info.nodes.push({
					category: category_id,
					name: co_expert.name,
					value: "合作年份: " + this_year,	// TODO 节点 value
					id: node_id
				});
				network_info.links.push({
					source: node_id,
					target: 0,	// 连线目标都是 0
					value: "关系强度: " + co_expert.co_score	// TODO 连线 value 随关系强度变化
				});
				node_id ++;
			}
        });
		category_id ++;
    });

	console.log(network_info);

	// 基于准备好的 dom，初始化 echarts 实例
	let myChart = echarts.init(document.getElementById('relationship_echarts'));

	// 指定图表的配置项和数据 http://echarts.baidu.com/examples/data/asset/data/les-miserables.gexf
	// app.title = '力引导布局';

	// myChart.showLoading();
	// myChart.hideLoading();

	// 设置初始只显示相关机构和最近一年的合作学者
	un_show_legend_list = {};
	network_info.categories.forEach(function (item, index) {
		if(index > 2) {
			un_show_legend_list[item.name] = false;
		}
    });

	// console.log(un_show_legend_list);

	// 指定图表的配置项和数据
	let option = {
		legend: {
			// 图例位置
			x: 'left',
			// 设置初始只显示相关机构和最近一年的合作学者
			selected: un_show_legend_list,
			// 图例的名称，必须和关系网类别中 name 相对应
			data: network_info.categories.map(function (item) {
				return item.name;
			})
		},
		series: [{
			type: 'graph',		// 关系图
			// name: "合作关系",		// 系列名称，用于tooltip的显示，legend 的图例筛选，在 setOption 更新数据和配置项时用于指定对应的系列
			layout: 'force',	// 图的布局，类型为力导图，'circular' 采用环形布局
			legendHoverLink: true,	// 是否启用图例 hover(悬停) 时的联动高亮
			hoverAnimation: true,	// 是否开启鼠标悬停节点的显示动画
			coordinateSystem: null,	// 坐标系可选
			xAxisIndex: 0, 		// x轴坐标 有多种坐标系轴坐标选项
			yAxisIndex: 0,		// y轴坐标
			roam: false,		// 是否开启鼠标缩放和平移漫游。默认不开启。如果只想要开启缩放或者平移，可以设置成 'scale' 或者 'move'。设置成 true 为都开启
			nodeScaleRatio: 0,	// 鼠标漫游缩放时节点的相应缩放比例，当设为0时节点不随着鼠标的缩放而缩放
			draggable: true,	// 节点是否可拖拽，只在使用力引导布局的时候有用。
			focusNodeAdjacency: true,	// 是否在鼠标移到节点上的时候突出显示节点以及节点的边和邻接节点。
			// animation: false,
			label: {
				normal: {
					show: true,
					position: 'right'
				}
			},
			force: {
				layoutAnimation: true,
				// xAxisIndex : 0,	// x轴坐标, 有多种坐标系轴坐标选项
				// yAxisIndex : 0,	// y轴坐标
				gravity: 0.03,		//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
				edgeLength: 70,		//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
				repulsion: 150		//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
			},
			// node数据
			data: network_info.nodes.map(function (node, index) {
				node.id = index;
				return node;
			}),
			// 关系网类别，可以写多组
			categories: network_info.categories,
			// link数据
			edges: network_info.links,
			// 边两端的标记类型，可以是一个数组分别指定两端，也可以是单个统一指定。默认不显示标记，常见的可以设置为箭头，
			// 如：edgeSymbol: ['circle', 'arrow']
			edgeSymbol: ['none', 'none'],
			edgeSymbolSize: 10	// 边两端的标记大小，可以是一个数组分别指定两端，也可以是单个统一指定。

			// symbol:'roundRect',	// 关系图节点标记的图形。ECharts 提供的标记类型包括 'circle'(圆形), 'rect'（矩形）,
			// 'roundRect'（圆角矩形）, 'triangle'（三角形）, 'diamond'（菱形）, 'pin'（大头针）, 'arrow'（箭头）.
			// 也可以通过 'image://url' 设置为图片，其中 url 为图片的链接。'path:// 这种方式可以任意改变颜色并且抗锯齿

			// symbolSize:10 ,		// 也可以用数组分开表示宽和高，例如 [20, 10] 如果需要每个数据的图形大小不一样，可以设置为如下格式的回调函数：(value: Array|number, params: Object) => number|Array
			// symbolRotate:,		// 关系图节点标记的旋转角度。注意在 markLine 中当 symbol 为 'arrow' 时会忽略 symbolRotate 强制设置为切线的角度。
			// symbolOffset:[0,0],	// 关系图节点标记相对于原本位置的偏移。[0, '50%']
		}],
		tooltip: {
			show: true,	// 默认显示
			showContent :true,	// 是否显示提示框浮层
			trigger: 'item',	// 触发类型，默认数据项触发
			triggerOn: 'click',	// 提示触发条件，mousemove鼠标移至触发，还有click点击触发
			alwaysShowContent: false,	// 默认离开提示框区域隐藏，true为一直显示
			showDelay: 0,		// 浮层显示的延迟，单位为 ms，默认没有延迟，也不建议设置。在 triggerOn 为 'mousemove' 时有效。
			hideDelay: 200,		// 浮层隐藏的延迟，单位为 ms，在 alwaysShowContent 为 true 的时候无效。
			enterable: false,	// TODO 鼠标是否可进入提示框浮层中，默认为false，如需详情内交互，如添加链接、按钮，可设置为 true。
			position: 'right',	// 提示框浮层的位置，默认不设置时位置会跟随鼠标的位置。只在 trigger 为'item'的时候有效。
			confine: false,		//是否将 tooltip 框限制在图表的区域内。外层的 dom 被设置为 'overflow: hidden'，或者移动端窄屏，
			// 导致 tooltip 超出外界被截断时，此配置比较有用。
			transitionDuration: 0.4,	// 提示框浮层的移动动画过渡时间，单位是 s，设置为 0 的时候会紧跟着鼠标移动。
		}
	};

	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(option);
}


// 从当前的关系网络选项，获取 node_list
function getNodeListD3(co_expert_array) {
	result_ajax = result_ajax_detail;
	// 获取当前所选的年份
	let relationship_year = ''
	jq_relationship_year = $('select#relationship_year');
	relationship_year = jq_relationship_year.val()

	// 初始状态选择最近的一年的论文合作学者
	jq_relationship_type = $('select#relationship_type option:selected');
	relationship_type = jq_relationship_type.val();

	// 关系网络文字描述
	let jq_relationship_div = $('#relationship_div');
	let node_list = [];
	if(relationship_type === 'co_expert_paper') {
		// 如果当前选择了"论文合作学者"，那么使年份选择框可用
		if(jq_relationship_year.attr('disabled') != false) {
			jq_relationship_year.attr('disabled', false);
		}
		// 点击学者名跳转到该学者详情页
		let relationship_html = '<h3>' + relationship_year + '年 论文合作学者</h3><p>';
		co_expert_array.forEach(function (item, index) {
			// 对该学者在所学年份的论文合作学者设置跳转锚点
			if(item.co_year === relationship_year) {
				relationship_html += '<a onclick="jumpToAnotherResearcher(' + item.id + ')">' +
					item.name + '</a>' + ' , ';
				// TODO 目前仅把学者 id 加入到 node_list
				node_list.push(item.id);
			}
		});
		relationship_html = relationship_html.substring(0, (relationship_html.length - 3));	// 截去字符串最后的' , '
		relationship_html += '</p>';

		jq_relationship_div.empty();
		jq_relationship_div.append(relationship_html);
	} else if(relationship_type === 'co_agency') {
		// 如果当前选择了"相关机构"，那么使年份选择框不可用
		if(jq_relationship_year.attr('disabled') != true) {
			jq_relationship_year.attr('disabled', true);
		}
		let co_agency_string = result_ajax.expert_academic.co_agency;
		co_agency_string = co_agency_string.replace(/\[/g, '');
		co_agency_string = co_agency_string.replace(/]/g, '');
		co_agency_string = co_agency_string.replace(/'/g, '');
		co_agency_string = co_agency_string.replace(/ /g, '');

		node_list = co_agency_string.split(',');

		// TODO 点击跳转机构页
		let relationship_html = '<h3>相关机构</h3><p>';
		node_list.forEach(function (item, index) {
			relationship_html += item + ' , ';
		});
		relationship_html = relationship_html.substring(0, (relationship_html.length - 3));	// 截去字符串最后的' , '
		relationship_html += '</p>';

		jq_relationship_div.empty();
		jq_relationship_div.append(relationship_html);
    }

    // console.log(node_list);
	return node_list;
}


// D3.js 绘力导向图
function drawNetworkD3(node_list) {
	result_ajax = result_ajax_detail;
	// 关系网络json
	let node_id = 0;
	let relationship_network = {
		"nodes": {
			"center_node": [
				{
					"id": node_id,
					"node_expert_id": result_ajax.expert_basic.id,
					"group": 0,
					"color": 'black'
				}
			],
			"relative_node": [
			]
		},
		"links": {
			"relative_link": [
			]
		}
	};

	// 把结点写入 relationship_network
	node_id = 1;
	node_list.forEach(function (item, index) {
		let co_node = {};
		co_node.id = node_id ++;
		co_node.node_expert_id = item;
		co_node.group = 1;
		co_node.color = "#add8e6";	// light blue TODO 换成专家头像
		relationship_network.nodes.relative_node.push(co_node);
    });

	// 把边写入 relationship_network
	node_id = 1;
	node_list.forEach(function (item, index) {
		let co_link = {};
		co_link.source = node_id ++;
		co_link.target = 0;
		co_link.stroke_width = 1; // TODO 根据关系紧密程度来设置线段
		relationship_network.links.relative_link.push(co_link);
    });

	console.log(relationship_network);

	let jq_relationship_canvas_div = $('#relationship_picture_div');

	let jq_relationship_svg = $('#relationship_svg');
	jq_relationship_svg.empty();

	relationship_svg_html = '<defs>' +
        '<pattern id="default_expert_avatar" width="100%" height="100%" patternContentUnits="objectBoundingBox">' +
        '<image width="1" height="1" xlink:href="static/image/default_expert_image.png" />' +
        '</pattern>' +
        '<style>circle, rect {stroke: #ff9900; stroke-width: 5px;}' +
        '</style></defs>';

	jq_relationship_svg.append(relationship_svg_html);

	let width = jq_relationship_canvas_div.width();
	let height = window.innerHeight / 2;
	jq_relationship_svg.width(width);
	jq_relationship_svg.height(height);

	let svg = d3.select("#relationship_svg");

	let simulation = d3.forceSimulation()
		.force("link", d3.forceLink().id(function(item, index) {
			return item.id;
		}).distance(height / 8 * 3))
		.force("charge", d3.forceManyBody())
		.force("center", d3.forceCenter(width / 2, height / 2));

	let all_nodes = [];
	all_nodes = all_nodes.concat(relationship_network.nodes.center_node);
	all_nodes = all_nodes.concat(relationship_network.nodes.relative_node);

	let agency_link = relationship_network.links.relative_link;
	let all_links = [];
	all_links = all_links.concat(agency_link);

	console.log(all_nodes);
	console.log(all_links);

	simulation
		.nodes(all_nodes)
		.on("tick", Ticked);

	simulation.force("link")
		.links(all_links);

	let link = svg.append("g")
		.attr("class", "svg_links")
		.selectAll("line")
		.data(all_links)
		.enter().append("line")
		// TODO stroke-width 属性可以用于表达关系紧密度
		.attr("stroke-width", function(d) {return d.stroke_width;})
		.attr("stroke", "#aaa");

    let node = svg.append("g")
		.attr("class", "svg_nodes")
		.selectAll("circle")
		.data(all_nodes)
		.enter().append("circle")	// 添加圆圈
		.attr("r", 25)
		// .attr("fill", function(d) {return d.color;})
		.attr("fill", "url(#default_expert_avatar)") // TODO 用头像填充照片
		.call(d3.drag()
			.on("start", dragstarted)
			.on("drag", dragged)
			.on("end", dragended)
		).text(function (d) {
			return d.node_expert_id;
        });

    function Ticked() {
		link
			.attr("x1", function(d) {return d.source.x;})
			.attr("y1", function(d) {return d.source.y;})
			.attr("x2", function(d) {return d.target.x;})
			.attr("y2", function(d) {return d.target.y;});

		node
			.attr("cx", function(d) {return d.x;})
			.attr("cy", function(d) {return d.y;});
    }

	function dragstarted(d) {
       if (!d3.event.active) simulation.alphaTarget(0.3).restart();
       d.fx = d.x;
       d.fy = d.y;
	}
	function dragged(d) {
	   d.fx = d3.event.x;
	   d.fy = d3.event.y;
	}
	function dragended(d) {
	   if(!d3.event.active) simulation.alphaTarget(0);
	   d.fx = null;
	   d.fy = null;
	}

	// TODO 给 svg circle 添加文字
	// let jq_svg_circle = $('#relationship_picture_div g.svg_nodes');
    // let jq_svg_line = $('#relationship_picture_div g.svg_links line');
    // jq_svg_circle.append('<text x="50" y="50" text-anchor="middle" stroke="#51c5cf" stroke-width="2px" dy=".3em">center</text>')
    // let svg_circle = d3.select('#relationship_svg g.svg_nodes circle');
    // let svg_line = d3.select('#relationship_svg g.svg_links line');
    // svg_circle.selectAll("circle")
		// .data(all_nodes)
		// .enter().append("text")	// 添加文字
		// .attr("x", "100px").attr("y", "100px").attr("text-anchor", "middle")
		// .attr("stroke", "#51c5cf").attr("stroke-width", "2px").attr("dy", ".3em")
		// .text("center")

	// 给容器增加边框
	jq_relationship_canvas_div.css({"border": "1px solid #aaa"});
}


// TODO 用户登录
function logIn() {
	'use strict';
	let jq_username = $('#username');
	let jq_password = $('#password');
	let jq_a = $('#menu ul.actions > li > a');

	let username = jq_username.val().trim();
	let password = jq_password.val().trim();
	let choice = jq_a.text();

	if(choice === '注销') {
		if(confirm('确认注销')) {
			jq_username.show();
			jq_password.show();
			jq_a.text('登录');
		}
	} else if(choice === '登录') {
		if(!username || username === '') {
			$.toast({
				text: "请您输入账号！",
				showHideTransition: 'slide',
				bgColor: 'orange',
				textColor: '#e0e0e0',
				allowToastClose : false,
				hideAfter: 2000,
				stack: 5,
				textAlign: 'center',
				position: 'mid-center'
			});
			jq_username.focus();
		} else if(!password || password === '') {
			$.toast({
				text: "请您输入密码！",
				showHideTransition: 'slide',
				bgColor: 'orange',
				textColor: '#e0e0e0',
				allowToastClose : false,
				hideAfter: 2000,
				stack: 5,
				textAlign: 'center',
				position: 'mid-center'
			});
			jq_password.focus();
		} else {
			// TODO 判断逻辑交由后台处理
			if(username === 'yin' && password === 'yuwei') {
				jq_username.hide();
				jq_password.hide();
				jq_a.text('注销');
				$.toast({
					text: "登录成功",
					showHideTransition: 'fade',
					bgColor: 'lightblue',
					textColor: '#e0e0e0',
					allowToastClose : false,
					hideAfter: 2000,
					stack: 5,
					textAlign: 'center',
					position: 'mid-center'
				});
			} else {
				$.toast({
					text: "登录失败",
					showHideTransition: 'plain',
					bgColor: 'red',
					textColor: '#e0e0e0',
					allowToastClose : false,
					hideAfter: 2000,
					stack: 5,
					textAlign: 'center',
					position: 'mid-center'
				});
			}
		}
	}

	return true;
}


// TODO 关注本页学者
function star_expert() {
	'use strict';
	// let data = result_ajax_detail;
	return true;
}


function isChrome() {
	'use strict';
	let ua = navigator.userAgent;
	return (ua.indexOf("Chrome") > -1);
}

(function($) {
	'use strict';

	/*
		Toast使用说明

		text：消息提示框的内容.
		showHideTransition：消息提示框的动画效果。可取值：plain, fade, slide.
		bgColor：背景颜色.
		textColor：文字颜色.
		allowToastClose：是否显示关闭按钮.
		hideAfter：设置为false则消息提示框不自动关闭。设置为一个数值则在指定的毫秒之后自动关闭消息提示框.
		stack：消息栈.
		textAlign：文本对齐：left, right, center.
		position：消息提示框的位置：bottom-left, bottom-right, bottom-center,
				top-left, top-right, top-center, mid-center.
	*/

	window.onload = function () {
        // 获取id参数
		let expert_id;
        let url_data = window.location.search;
        let index_start = url_data.indexOf("id=") + 3;
        let index_end = url_data.indexOf("#", index_start);
        if(index_end === -1) {
            expert_id = url_data.substring(url_data.lastIndexOf("id=") + 3, url_data.length);
        } else {
            expert_id = url_data.substring(url_data.lastIndexOf("id=") + 3, index_end);
        }
        // 检验id合法性(全是数字)
        if(isNaN(expert_id)) {
            alert("Error: id参数不合法");
            console.log("Error: id参数不合法");
            return false;
        }
        // AJAX获得数据,成功后渲染页面
		query_detail_ajax(expert_id);
    };

	// Chrome浏览器处理
	if (isChrome() && window.history && window.history.pushState) {
		$(window).on('popstate', function () {
			window.location.href = window.document.referrer;
			window.history.go(-2);
		});
		window.history.pushState(location.href, document.title);
	}

	// 防止页面后退
	history.pushState(null, null, document.URL);
	window.addEventListener('popstate', function () {
		history.pushState(null, null, document.URL);
	});

    // // 关系网络的 select option 改变时，更改力导向图
    // $('select.relationship_select').change(function () {
		// result_ajax = result_ajax_detail;
		// // 获取所有相关专家数据
		// let co_expert_array = [];
		// result_ajax.co_experts_info.forEach(function (item, index) {
		// 	co_expert_array.push(JSON.parse(item));
		// });
		// console.log(co_expert_array);
    //
		// // 绘力导向图
		// drawNetworkEcharts(co_expert_array);
    // });
})(jQuery);