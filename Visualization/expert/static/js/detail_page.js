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
			console.log(endDate - startDate);

			console.log("$.ajax beforeSend, state = " + xhr.status);
			// 出现loading动画
			$('#intro .load-container').css({"display": "block"});
		},
		success: function(result, status, xhr) {
			endDate = new Date();
			console.log(endDate - startDate);

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
					hideAfter: 2000,
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
			console.log(endDate - startDate);

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


function render_detail_page(result_ajax) {
    'use strict';
    // 绘制专家关系图
    relationshipNet(result_ajax);

    // 增添其它信息
    let jq_researcher_academic_content = $('#researcher_academic_content > table > tbody > tr:first-child');
    let jq_this_researcher_name = $('.this_researcher_name');
    let jq_this_researcher_university = $('#intro .this_researcher_university');
    let jq_this_researcher_college = $('#intro .this_researcher_college');
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
			hideAfter: 800,
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
			hideAfter: 800,
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
			hideAfter: 800,
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
			hideAfter: 800,
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


// 绘制专家关系图
// TODO 调整初始图像美观度;增添文字描述;增添链接跳转;分类显示合作学者/合作机构.
function relationshipNet(result_ajax) {
	// 获取数据库中存在的相关专家数据(有的相关专家并未在数据库中存在)
	let co_experts_info = [];
	result_ajax.co_experts_info.forEach(function (item, index) {
		co_experts_info.push(JSON.parse(item));
    });

	console.log(co_experts_info);

	// 获取expert_academic表内的相关专家&相关机构
	let co_expert_string = result_ajax.expert_academic.co_expert;
	co_expert_string = co_expert_string.replace(/\[/g, '');
	co_expert_string = co_expert_string.replace(/]/g, '');
	co_expert_string = co_expert_string.replace(/'/g, '');
	co_expert_string = co_expert_string.replace(/ /g, '');

	let co_agency_string = result_ajax.expert_academic.co_agency;
	co_agency_string = co_agency_string.replace(/\[/g, '');
	co_agency_string = co_agency_string.replace(/]/g, '');
	co_agency_string = co_agency_string.replace(/'/g, '');
	co_agency_string = co_agency_string.replace(/ /g, '');

	let co_expert_array = co_expert_string.split(',');
	let co_agency_array = co_agency_string.split(',');

	// console.log(co_expert_array);
	// console.log(co_agency_array);

	let node_id = 0;
	let researchers_json = {
		"nodes": {
			"center_node": [
				{"id": node_id, "node_expert_id": result_ajax.expert_basic.id, "group": 0, "color": 'black'}
			],
			"relative_researcher_node": [
			],
			"relative_agency_node": [
			]
		},
		"links": {
			"relative_researcher_link": [
			],
			"relative_agency_link": [
			]
		}
	};

	// 把结点写入researchers_json
	co_expert_array.forEach(function (item, index) {
		let co_expert_node = {};
		co_expert_node.id = ++ node_id;
		co_expert_node.node_expert_id = item;
		co_expert_node.group = 1;
		co_expert_node.color = "#add8e6";	//light blue
		researchers_json.nodes.relative_researcher_node.push(co_expert_node);
    });
	co_agency_array.forEach(function (item, index) {
		let co_agency_node = {};
		co_agency_node.id = ++ node_id;
		co_agency_node.node_expert_id = item;
		co_agency_node.group = 2;
		co_agency_node.color = "#ffc0cb";	// pink
		researchers_json.nodes.relative_agency_node.push(co_agency_node);
    });

	// 把边写入researchers_json
	node_id = 1;
	co_expert_array.forEach(function (item, index) {
		let co_expert_link = {};
		co_expert_link.source = node_id ++;
		co_expert_link.target = 0;
		co_expert_link.stroke_width = 1;
		researchers_json.links.relative_researcher_link.push(co_expert_link);
    });
	co_agency_array.forEach(function (item, index) {
		let co_agency_link = {};
		co_agency_link.source = node_id ++;
		co_agency_link.target = 0;
		co_agency_link.stroke_width = 2;
		researchers_json.links.relative_agency_link.push(co_agency_link);
    });

	console.log(researchers_json);

	let jq_relationship_canvas_div = $('#relationship_picture_div');

	let jq_relationship_svg = $('#relationship_svg');
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

	// console.log(researchers_json);

	let all_nodes = [];
	all_nodes = all_nodes.concat(researchers_json.nodes.center_node);
	all_nodes = all_nodes.concat(researchers_json.nodes.relative_researcher_node);
	all_nodes = all_nodes.concat(researchers_json.nodes.relative_agency_node);

	let researcher_link = researchers_json.links.relative_researcher_link;
	let agency_link = researchers_json.links.relative_agency_link;
	let all_links = [];
	all_links = all_links.concat(researcher_link);
	all_links = all_links.concat(agency_link);

	// console.log(all_nodes);
	// console.log(all_links);

	simulation
		.nodes(all_nodes)
		.on("tick", Ticked);

	simulation.force("link")
		.links(all_links);

	let link = svg.append("g")
		.attr("class","svg_links")
		.selectAll("line")
		.data(all_links)
		.enter().append("line")
		// TODO stroke-width 属性可以用于表达关系紧密度
		.attr("stroke-width",function(d) {return d.stroke_width;})
		.attr("stroke", "#aaa");

    let node = svg.append("g")
		.attr("class","svg_nodes")
		.selectAll("circle")
		.data(all_nodes)
		.enter().append("circle")
		.attr("r",20)
		.attr("fill",function(d) {return d.color;})
		.call(d3.drag()
				.on("start",dragstarted)
				.on("drag",dragged)
				.on("end",dragended)
		);

    function Ticked() {
		link
			.attr("x1",function(d) {return d.source.x;})
			.attr("y1",function(d) {return d.source.y;})
			.attr("x2",function(d) {return d.target.x;})
			.attr("y2",function(d) {return d.target.y;});

		node
			.attr("cx",function(d) {return d.x;})
			.attr("cy",function(d) {return d.y;});
    }

	function dragstarted(d) {
       if (!d3.event.active) simulation.alphaTarget(0.3).restart();
       d.fx=d.x;
       d.fy=d.y;
	}
	function dragged(d) {
	   d.fx=d3.event.x;
	   d.fy=d3.event.y;
	}
	function dragended(d) {
	   if(!d3.event.active) simulation.alphaTarget(0);
	   d.fx=null;
	   d.fy=null;
	}

	// 给容器增加边框
	jq_relationship_canvas_div.css({"border": "1px solid #aaa"});

    // TODO 关系网络文字描述
	let html_template = '<p>';
	let jq_relationship_expert_div = $('#relationship_expert_div');
	// 对于academic_info表中该学者的合作学者
	co_expert_array.forEach(function (item, index) {
		// TODO 目前数据库中可能不存在该合作学者,故做此处理(该步骤在充实数据库后可以优化)
		let existTag = false;
		for(let i = 0 ; i < co_experts_info.length ; i++) {
			if(item === co_experts_info[i].id) {
				html_template += '<a onclick="jumpToAnotherResearcher(' + item + ')">' +
					co_experts_info[i].name + '</a>' + ' , ';
				existTag = true;
				break;
			}
		}
		if(!existTag) {
			html_template += item + ' , ';
		}
    });
	// 截去字符串最后的' , '
	html_template = html_template.substring(0, (html_template.length - 3));
	html_template += '</p>';
	jq_relationship_expert_div.append(html_template);

	// TODO 由于数据库中并无机构信息,故暂不设置点击跳转机构详情(可设计:点击相当于主页搜索该机构,至搜索结果页)
	let jq_relationship_agency_div = $('#relationship_agency_div');
	co_agency_array.forEach(function (item, index) {
		jq_relationship_agency_div.append('<p>' + item + '</p>');
    });

	// TODO 关系网络分析

	// TODO 点击相关学者进行跳转

	// TODO 用按钮控制show or hide图中的结点
	// function ChangeLinks() {
	// 	context.clearRect(0, 0, width, height);
	// }

	// function Ticked() {
	// 	context.clearRect(0, 0, width, height);
    //
	// 	context.beginPath();
	// 	all_nodes.forEach(DrawNode);
	// 	context.fill();
	// 	context.strokeStyle = "#fff";
	// 	context.stroke();
    //
	// 	context.beginPath();
	// 	all_links.forEach(DrawLink);
	// 	context.strokeStyle = "#aaa";
	// 	context.stroke();
	// }

	// function DragSubject() {
	// 	return simulation.find(d3.event.x, d3.event.y);
	// }
    //
	// function DragStart() {
	// 	if (!d3.event.active) simulation.alphaTarget(0.3).restart();
	// 	d3.event.subject.fx = d3.event.subject.x;
	// 	d3.event.subject.fy = d3.event.subject.y;
	// }
    //
	// function Drag() {
	// 	d3.event.subject.fx = d3.event.x;
	// 	d3.event.subject.fy = d3.event.y;
	// }
    //
	// function DragEnd() {
	// 	if (!d3.event.active) simulation.alphaTarget(0);
	// 	d3.event.subject.fx = null;
	// 	d3.event.subject.fy = null;
	// }

	// function DrawLink(item, index) {
	// 	context.moveTo(item.source.x, item.source.y);
	// 	context.lineTo(item.target.x, item.target.y);
	// }
    //
	// function DrawNode(item, index) {
    //
	// 	let node_color;
	// 	let node_radius;
    //
	// 	if(item.group === 0) {
	// 		// 绘制center(专家)
	// 		node_color = 'orange';
	// 		node_radius = 30;
	// 	} else if(item.group === 1) {
	// 		// 绘制relative_researcher_node(相关专家)
	// 		node_color = 'lightblue';
	// 		node_radius = 30;
	// 	} else if(item.group === 2) {
	// 		// 绘制relative_agency_node(相关机构)
	// 		node_color = 'pink';
	// 		node_radius = 30;
	// 	} else {
	// 		console.log("function DrawNode Error: index = " + index);
	// 		console.log(item);
	// 		node_color = 'black';
	// 		node_radius = 20;
	// 	}
	// 	context.beginPath();
	// 	context.moveTo(item.x + node_radius, item.y);
	// 	context.arc(item.x, item.y, node_radius, 0, 2 * Math.PI);
	// 	context.closePath();
	// 	context.fillStyle = node_color;
	// 	context.fill();
	// }
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
				hideAfter: 1000,
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
				hideAfter: 1000,
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
					hideAfter: 1000,
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
					hideAfter: 1000,
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
})(jQuery);