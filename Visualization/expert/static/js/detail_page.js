// JavaScript Document

/* jshint esversion: 6 */

let result_ajax_detail = {};

// 查询专家详情
function query_detail_ajax(expert_id) {
	'use strict';

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
			console.log("$.ajax beforeSend, state = " + xhr.status);
			// 出现loading动画
			$('#intro .load-container').css({"display": "block"});
		},
		success: function(result, status, xhr) {
			console.log("$.ajax success, state = " + xhr.status);
			// 隐藏loading动画
			$('#intro .load-container').css({"display": "none"});

			if(!result || result === "" || result.length === 0) {
				// TODO
			    alert("抱歉，该专家无信息。");
				console.log("抱歉，该专家无信息。");
				return false;
			}

			// 解析JSON数据
			result_ajax_detail.expert_basic = JSON.parse(result.expert_basic);
			result_ajax_detail.expert_academic = JSON.parse(result.expert_academic);
			result_ajax_detail.papers = JSON.parse(result.papers);

			console.log(result_ajax_detail);
			console.log(JSON.parse(result_ajax_detail.papers[0]));

			result = result_ajax_detail;

			// 使用数据渲染页面
            render_detail_page(result);

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
    let jq_this_researcher_resume = $('#researcher_resume div.content');

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

    // 若数据库中有学者的头像,则将页面中的默认头像更换掉
	let expert_image = result_ajax.expert_basic.img_url;
	if(expert_image && expert_image !== '') {
		jq_this_researcher_image.attr({"src": expert_image});
	}

	// 学者简历信息
	let expert_resume = result_ajax.expert_basic.resume;
	jq_this_researcher_resume.empty();
	if(expert_resume && expert_resume !== '') {
		jq_this_researcher_resume.append('<p>' + expert_resume + '</p>');
	} else {
		jq_this_researcher_resume.append('<p>无该学者简历数据.</p>');
	}

    // 展示全部(or被引量最高的五篇)论文
    let paper_item;
    html_template = '';
    result_ajax.papers.forEach(function (item, index) {
    	let paper_authors = [];

    	// 解析数据为JSON格式
    	paper_item = JSON.parse(item);

    	// 获取作者信息
		if(paper_item.author1 && (paper_item.author1 !== '')) {
			paper_authors.push(paper_item.author1);
		}
		if(paper_item.author2 && (paper_item.author2 !== '')) {
			paper_authors.push(paper_item.author2);
		}
		if(paper_item.author3 && (paper_item.author3 !== '')) {
			paper_authors.push(paper_item.author3);
		}
		if(paper_item.author4 && (paper_item.author4 !== '')) {
			paper_authors.push(paper_item.author4);
		}
		if(paper_item.author5 && (paper_item.author5 !== '')) {
			paper_authors.push(paper_item.author5);
		}

		// 设置html结点
    	html_template += '<li><article><header><h3><a href="#">' + paper_item.title + '</a></h3></header>';

		// 设置作者
		html_template += '<p>';
		let i;
		for(i = 0 ; i < paper_authors.length - 1 ; i++) {
			html_template += '<a onclick="jumpToAnotherResearcher(' + paper_authors[i] + ')">' +
				paper_authors[i] + '</a>' + ',';
		}
		html_template += '<a onclick="jumpToAnotherResearcher(' + paper_authors[i] + ')">' +
			paper_authors[i] +'</a>' + ' | ';

		// 设置其它论文信息
		html_template += (paper_item.type || '') + ' | ' + paper_item.source + '</p>';

		html_template += '<p><strong>' + '摘要</strong>: ' + paper_item.abstract + '</p>';

		html_template += '<p><strong>' + '关键字</strong>: ' + paper_item.keyword + '</p>';

		html_template += '</article></li>';
    });
    jq_this_researcher_papers.empty();
    jq_this_researcher_papers.append(html_template);
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
	// 获取相关专家&相关机构
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

	// let canvas = document.querySelector("#relationship_canvas"),
	// 	context = canvas.getContext("2d");
    //
	let jq_relationship_canvas_div = $('#relationship_picture_div');
	// canvas.width = jq_relationship_canvas_div.width();
	// canvas.height = window.innerHeight / 2;
	// canvas.style.border = "1px solid #000";
    //
	// let width = canvas.width;
	// let height = canvas.height;

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

	// d3.select(canvas)
	// 	.call(d3.drag()
	// 		.container(canvas)
	// 		.subject(DragSubject)
	// 		.on("start", DragStart)
	// 		.on("drag", Drag)
	// 		.on("end", DragEnd)
	// 	);

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
	let jq_relationship_expert_div = $('#relationship_expert_div > p');
	jq_relationship_expert_div.empty();
	jq_relationship_expert_div.append(co_expert_string);

	let jq_relationship_agency_div = $('#relationship_agency_div > p');
	jq_relationship_agency_div.empty();
	jq_relationship_agency_div.append(co_agency_string);

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
        // AJAX获得数据
		query_detail_ajax(expert_id);
    };

	if (isChrome() && window.history && window.history.pushState) {
		 $(window).on('popstate', function () {
			 window.location.href = window.document.referrer;
			 window.history.go(-2);
		 });
		 window.history.pushState(location.href, document.title);
	 }
})(jQuery);