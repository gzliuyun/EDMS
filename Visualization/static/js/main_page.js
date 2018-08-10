// JavaScript Document

/* jshint esversion: 6 */

var result_ajax;
var result_page_total = 0;
var result_page_now = 0;


function query_http(qi, qt, qs, r, f, rc, org) {
	'use strict';
	var server_url = "expert/list";
	
	var post_data = {};
	if(qt === "normal") {
		post_data.query_input = qi;
		post_data.query_type = qt;
		post_data.query_selection = qs;
	} else if(qt === "advanced") {
		post_data.query_type = qt;
		post_data.researcher_input = r;
		post_data.field_input = f;
		post_data.research_content_input = rc;
		post_data.organization_input = org;
	} else {
		//隐藏loading动画
		$('.load-container').css({"display": "none"});
		return false;
	}
	
	// HTTP POST (JQuery Ajax)
	$.ajax({
		type: "GET",
		url: server_url,
		data: post_data,
		//crossDomin: true,
		//dataType: "jsonp",
		//jsonp: "jsonp_callback",
		//jsonpCallback: "jsonpCallbackFunction",
		dataType: "json",
		//async: true,    // 使用同步操作
		//timeout: 50000, // 超时时间：50秒
		beforeSend: function(xhr) {
//		    alert("server_url=" + server_url + "&post_data=" +post_data.query_input);
			// 出现loading动画
			$('.load-container').css({"display": "block"});
			// 隐藏页面按钮
			$('#query_result_page').css({"display": "none"});
		},
		success: function(result, status, xhr) {
			//alert('HTTP GET Success! normal_query: ' + 'result=' + result);
			
			// 隐藏loading动画
			$('.load-container').css({"display": "none"});

			if(!result || result === "" || result.length === 0) {
				// 清空researcher_result_list里面的所有内容
				$('.researcher_result_list').empty();
				// 提示无搜索结果
				var html_template = '<p id="search_result_tag">抱歉，无搜索结果，请输入其它关键词以查询。</p>';
				// 增添子元素到researcher_result_list结点
				$('.researcher_result_list').append(html_template);
				return false;
			} else {
				result_page_total = Math.floor(result.length / 20) + 1;
			}
			
			result_ajax = JSON.parse("[" + result + "]");
			result = result_ajax;
			result_page_now = 1;

			// 清空researcher_result_list里面的所有内容
			$('.researcher_result_list').empty();

			// 对返回结果的每个元素，增添到html_template里
			var html_template = '<p id="search_result_tag">搜索结果（点击以查看专家详细信息）：</p>' +
				'<p id="search_result_info">共 ' + result.length +
				' 条结果，分 ' + result_page_total + ' 页显示，' +
				'当前为第 ' + result_page_now + ' 页。</p><ul>';
			

			// 先渲染第一页，至多20位专家学者
			for(var i = 0 ; i < 20 && i < result.length ; i++) {
				// 判断专家有没有头像URL
				if(!result[i].img_url || result[i].img_url === "") {
					html_template += '<li>' +
						// 使用默认头像
						'<img src="static/image/edms_logo_image.png" alt="researcher image" />' +
						'<a href="show_page?id=' + result[i].id + '" id="researcher_' +
						result[i].id + '">' + result[i].name + '</a>' +
						'<p><strong>学校</strong>：' + result[i].university +
						'；<br /><strong>学院</strong>：' + result[i].college +
						// 只展示数据库中的第一个研究方向
						'；<br /><strong>研究方向</strong>：';
					if(!result[i].theme_list || result[i].theme_list === "") {
					    html_template += '无。</p>' + '</li>';
					} else {
						//html_template += result[i].theme_list.split("、", 1)[0] + '。</p>' +
                        html_template += result[i].theme_list + '。</p>' +
						'</li>';
					}
				} else {
					html_template += '<li>' +
						'<img src="' + result[i].img_url + '" alt="researcher image" />' +
						'<a href="show_page?id=' + result[i].id + '" id="researcher_' +
						result[i].id + '">' + result[i].name + '</a>' +
						'<p><strong>学校</strong>：' + result[i].university +
						'；<br /><strong>学院</strong>：' + result[i].college +
						// 只展示数据库中的第一个研究方向
						'；<br /><strong>研究方向</strong>：';
					if(!result[i].theme_list || result[i].theme_list === "") {
					    html_template += '无。</p>' + '</li>';
					} else {
						//html_template += result[i].theme_list.split("、", 1)[0] + '。</p>' +
                        html_template += result[i].theme_list + '。</p>' +
						'</li>';
					}
				}
			}
			html_template += '</ul>';
			// 增添子元素到researcher_result_list结点
			$('.researcher_result_list').append(html_template);
			// 根据展示的数据量确定页数div的显示位置
			$('#query_result_page').css({"margin": 90 * ( Math.floor((i-1)/4)+1 ) - 20 + "px 0 0 0"});
			// 出现页数div
			$('#query_result_page').css({"display": "block"});
			// 标注当前页(第1页)
			//$('#query_result_page_1').attr("now", "yes");
			//$('#query_result_page_1').css({"background-color": "rgba(100, 149, 237, 0.8)"});
			$('#query_result_page_1').css("border", "3px solid #000");
			// 给新增的列表项加上动态效果
			$('.researcher_result_list > ul > li > a').mouseover(function () {
				//$(this).css({"background-color": "#6495ed"});
				$(this).css({"background-color": "rgba(0, 180, 70, 0.8)"});
				$(this).parent().find("p").animate({opacity: "show", top: "-100"}, "slow");
			}).mouseout(function () {
				//$(this).css({"background-color": "#232323"});
				$(this).css({"background-color": "rgba(0, 180, 70, 0.3)"});
				$(this).parent().find("p").animate({opacity: "hide", top: "-120"}, "fast");
			});
		},
		error: function(xhr, status, error) {
			// 隐藏loading动画
			$('.load-container').css({"display": "none"});
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

	/*
	$.get("expert/list", {
			"query_input": qi,
			"query_type": qt,
			"query_selection": qs
		}, function(result) {
		//alert('HTTP GET Success! normal_query: ' + 'result=' + result);

		//隐藏loading动画
		$('.load-container').css({"display": "none"});

		var result_list = {};
		result_list = result.split("{");
		result_list.shift();

		for(var i = 0 ; i < result_list.length ; i++) {
			result_list[i] = "{" + result_list[i];
		}

		result_ajax = result_list;

		// 清空query_result_list里面的所有内容
		$('#query_result_list').empty();

		// 对返回结果的每个元素，增添到html_template里
		var html_template = '<div class="researcher_result_list">' +
			'<p id="search_result_tag">搜索结果（点击以查看专家详细信息）：</p>' +
			'<p id="search_result_info">共 ' + result_list.length +
			' 条结果，分 ' + result_list.length / 20 + ' 页显示</p><ul>';

		var json_parse;
		// 先渲染第一页，至多20位专家学者
		for(i = 0 ; i < 20 && i < result_list.length ; i++) {
			json_parse = JSON.parse(result_list[i]);
			// 判断专家有没有头像URL
			if(!json_parse.img_url || json_parse.img_url === "") {
				html_template += '<li>' +
					// 使用默认头像
					'<img src="static/image/edms_logo_image.png" alt="researcher image" />' +
					'<a href="expert/show_page?id="' + json_parse.id + ' id="researcher_' +
					json_parse.id + '">A教授</a>' +
					'<p><strong>学校</strong>：' + json_parse.university +
					'；<br /><strong>学院</strong>：' + json_parse.college +
					// 只展示数据库中的第一个研究方向
					'；<br /><strong>研究方向</strong>：' + json_parse.theme_list.split("、", 1)[0] + '。</p>' +
					'</li>';
			} else {
				html_template += '<li>' +
					'<img src="' + json_parse.img_url + '" alt="researcher image" />' +
					'<a href="expert/show_page?id="' + json_parse.id + ' id="researcher_' +
					json_parse.id + '">A教授</a>' +
					'<p><strong>学校</strong>：' + json_parse.university +
					'；<br /><strong>学院</strong>：' + json_parse.college +
					// 只展示数据库中的第一个研究方向
					'；<br /><strong>研究方向</strong>：' + json_parse.theme_list.split("、", 1)[0] + '。</p>' +
					'</li>';
			}
		}
		html_template += '</ul></div>';
		//alert("html_template = " + html_template);
		// 增添子元素到query_result_list结点
		$('#query_result_list').append(html_template);
	});
	*/
}

// 输入控制
function query_function() {
	'use strict';
	var query_type = $("#query_type").val().trim();
	
	if(query_type === "normal") {
		console.log('query_function() query_input=' + query_input +
			  "&query_type=" + query_type +
			  "&query_selection=" + query_selection);
		var query_input = $("input[name='query_input']").val().trim();
		var query_selection = $("#query_selection").val().trim();
		if(!query_input || query_input === "" || !query_selection || query_selection==="") {
			return false;
		} else {
			query_http(query_input, query_type, query_selection);
		}
	} else if(query_type === "advanced") {
		var researcher = $("#researcher_input").val().trim();
		var field = $("#field_input").val().trim();
		var research_content= $("#research_content_input").val().trim();
		var organization = $("#organization_input").val().trim();
		console.log(
			'query_function() query_type=' + query_type +
			  "&researcher_input=" + researcher +
			  "&field_input=" + field +
			  "&research_content_input=" + research_content +
			  "&organization_input=" + organization);
		if ( (!researcher && !field && !research_content && !organization) ||
			(researcher==="" && field==="" && research_content==="" && organization==="") ) {
				return false;
		} else {
			query_http("", query_type, "", researcher, field, research_content, organization);
		}
	} else {
		return false;
	}
}

// 切换查询类型：普通查询or高级查询 (normal or advanced)
function toggle_query_type_function() {
	'use strict';
	var query_type = $('#query_type').val().trim();
	if(query_type === 'normal') {
		$('.load-container').css({"padding": "100px 0 20px 0"});
		$('#query_type').val('advanced');
		$('#query_type_button').css("border", "3px solid #000");
		// 禁用普通输入框
		$('#query_input').attr("disabled", true);
		$('#query_input').val("请在下方输入框键入关键字");
		$('#query_input').css({"background-color": "#b0b0b0"});
		// 增添输入框
		$('#advanced_input_list').css({"opacity": "0"});
		var html = $(
			'<span class="input_left"><p>学者姓名:</p><input type="text" id="researcher_input" name="researcher_input" value=""  placeholder="请输入专家学者姓名" /></span>' +
			'<span class="input_right"><p>所属机构:</p><input type="text" id="organization_input" name="organization_input"  placeholder="请输入学者所属机构" /></span><br />' +
			'<span class="input_left"><p>钻研领域:</p><input type="text" id="field_input" name="field_input" value="" placeholder="请输入学者钻研领域" /></span>' +
			'<span class="input_right"><p>研究内容:</p><input type="text" id="research_content_input" name="research_content_input" value="" placeholder="请输入学者研究内容" /></span>'
		);
		$('#advanced_input_list').append(html);
		$('#advanced_input_list').animate({opacity: 1}, 500);
		//html.fadeIn(800);
	} else {
		$('.load-container').css({"padding": "20px 0 20px 0"});
		$('#query_type').val('normal');
		$('#query_type_button').css("border", "1px solid #6495ed");
		// 启用普通输入框
		$('#query_input').attr("disabled", false);
		$('#query_input').val("");
		$('#query_input').css({"background-color": "transparent"});
		// 移除输入框
		$('#advanced_input_list').animate({opacity: 0}, 300, "linear", function(){
			$("#advanced_input_list").empty();
		});
	}
}


// 换页时，改变查询结果内容
function change_query_result_page() {
	'use strict';

	if(!result_ajax || result_ajax.length === 0 || result_ajax === "" ||
		parseInt(result_page_now, 10) <= 0 || parseInt(result_page_total, 10) <= 0 ||
		parseInt(result_page_now, 10) > parseInt(result_page_total, 10) ) {
		console.log('function change_query_result_page() error: global variables error.');
		return false;
	}
	
	var result = result_ajax;
	var result_total_page = result_page_total;
	var result_now_page = result_page_now;
	// 该页第一条json内容在result中的索引位置
	var content_start_index = (parseInt(result_now_page, 10) - 1) * 20;
	// 该页最后一条json内容在result中的索引位置
	var content_end_index;
	if( (content_start_index + 20) <= result.length ) {
		content_end_index = parseInt(content_start_index, 10) + 19;
	} else {
		content_end_index = parseInt(result.length, 10) - 1;
	}
	// 该页的元素总数
	var content_total = parseInt(content_end_index, 10) - parseInt(content_start_index, 10) + 1;

	// 清空researcher_result_list里面的所有内容
	$('.researcher_result_list').empty();

	// 对返回结果的每个元素，增添到html_template里
	var html_template = '<p id="search_result_tag">搜索结果（点击以查看专家详细信息）：</p>' +
		'<p id="search_result_info">共 ' + result.length +
		' 条结果，分 ' + result_total_page + ' 页显示，' +
		'当前为第 ' + result_now_page + ' 页。</p><ul>';

	// 渲染新页面
	for(var i = parseInt(content_start_index, 10) ; i <= parseInt(content_end_index, 10) ; i++) {
		// 判断专家有没有头像URL
		if(!result[i].img_url || result[i].img_url === "") {
			html_template += '<li>' +
				// 使用默认头像
				'<img src="static/image/edms_logo_image.png" alt="researcher image" />' +
				'<a href="show_page?id=' + result[i].id + '" id="researcher_' +
				result[i].id + '">' + result[i].name + '</a>' +
				'<p><strong>学校</strong>：' + result[i].university +
				'；<br /><strong>学院</strong>：' + result[i].college +
				// 只展示数据库中的第一个研究方向
				'；<br /><strong>研究方向</strong>：';
			if(!result[i].theme_list || result[i].theme_list === "") {
                html_template += '无。</p>' + '</li>';
            } else {
                //html_template += result[i].theme_list.split("、", 1)[0] + '。</p>' +
                html_template += result[i].theme_list + '。</p>' +
                '</li>';
            }
		} else {
			html_template += '<li>' +
				'<img src="' + result[i].img_url + '" alt="researcher image" />' +
				'<a href="show_page?id=' + result[i].id + '" id="researcher_' +
				result[i].id + '">' + result[i].name + '</a>' +
				'<p><strong>学校</strong>：' + result[i].university +
				'；<br /><strong>学院</strong>：' + result[i].college +
				// 只展示数据库中的第一个研究方向
				'；<br /><strong>研究方向</strong>：';
			if(!result[i].theme_list || result[i].theme_list === "") {
                html_template += '无。</p>' + '</li>';
            } else {
                //html_template += result[i].theme_list.split("、", 1)[0] + '。</p>' +
                html_template += result[i].theme_list + '。</p>' +
                '</li>';
            }
		}
	}
	html_template += '</ul>';
	// 增添子元素到researcher_result_list结点
	$('.researcher_result_list').append(html_template);
	// 根据展示的数据量确定页数div的显示位置
	$('#query_result_page').css({"margin": 90 * ( Math.floor((content_total-1)/4)+1 ) - 20 + "px 0 0 0"});
	// 给新增的列表项加上动态效果
	$('.researcher_result_list > ul > li > a').mouseover(function () {
		//$(this).css({"background-color": "#6495ed"});
		$(this).css({"background-color": "rgba(0, 180, 70, 0.8)"});
		$(this).parent().find("p").animate({opacity: "show", top: "-100"}, "slow");
	}).mouseout(function () {
		//$(this).css({"background-color": "#232323"});
		$(this).css({"background-color": "rgba(0, 180, 70, 0.3)"});
		$(this).parent().find("p").animate({opacity: "hide", top: "-120"}, "fast");
	});
}


function isChrome() {
	'use strict';
	var ua = navigator.userAgent;
	if(ua.indexOf("Chrome") > -1) {
		return true;
	} else {
		return false;
	}
}

$(function() {
	'use strict';

	// input框的enter事件绑定
	document.getElementById("query_input").onkeydown = function (event) {
		if(event.keyCode === "13") {	// 按下Enter键
			query_function();
		}
	};
	
	if (isChrome() && window.history && window.history.pushState) {
		 $(window).on('popstate', function () {
			 window.location.href=window.document.referrer;
			 window.history.go(-2);
		 });
		 window.history.pushState(location.href, document.title);
	 }

	//切换标签
	$('#query_selection_list ul li').click(function() {
		$(this).addClass('active').siblings().removeClass('active');
	});

	$('#researcher').click(function() {
		$('#researcher_word').addClass('active');
		$('#field_word').removeClass('active');
		$("#query_selection").val("researcher");
	});

	$('#field').click(function() {
		$('#researcher_word').removeClass('active');
		$('#field_word').addClass('active');
		$("#query_selection").val("field");
	});
	
	$('#research_content').click(function() {
		$('#researcher_word').removeClass('active');
		$('#field_word').removeClass('active');
		$("#query_selection").val("research_content");
	});

	$('#organization').click(function() {
		$('#researcher_word').removeClass('active');
		$('#field_word').removeClass('active');
		$("#query_selection").val("organization");
	});
	
	
	// hover: change background-color
	$('#query_button').mouseover(function () {
		$(this).css("background-color","#6495ed");
	}).mouseout(function () {
		$(this).css("background-color","#87cefa");
	});
	
	$('#query_type_button').mouseover(function () {
		$(this).css({"background-color": "#6495ed"});
	}).mouseout(function () {
		$(this).css({"background-color": "#87cefa"});
	});
	
	
	// 页面跳转按钮-鼠标悬停移开事件
	$('#query_result_page > ul > li > button').mouseover(function () {
		$(this).css({"background-color": "rgba(100, 149, 237, 0.8)"});
	}).mouseout(function () {
		$(this).css({"background-color": "rgba(100, 149, 237, 0.3)"});
	});
	
	// 页面跳转按钮-点击事件-上一页
	$('#query_result_page_pre').click(function() {
		// 获取当前两边的按钮所指页数
		var left_button = $('#query_result_page_1').val();
		//var right_button = $('#query_result_page_10').val();
		var i = 0;
		
		if(!result_page_now || result_page_now <= 0 || result_page_now > result_page_total) {
			console.log('pre_page_error! result_page_now is out of range.');
			//alert('pre_page_error! result_page_now is out of range.');
			return false;
		} else if(parseInt(result_page_now, 10) === 1) {
			alert('当前页已经是第一页了');
			return false;
		} else {
			if(left_button.toString() === result_page_now.toString()) {
				// 如果当前页是最左按钮所指的页面，则要调整全部按钮的值
				for(i = 1 ; i <= 10 ; i++) {
					$('#query_result_page_' + i).val( parseInt($('#query_result_page_' + i).val().toString(), 10) - 1 );
				}
				result_page_now = parseInt(result_page_now, 10) - 1;
				// change content
				change_query_result_page();
			} else if(parseInt(left_button, 10) < parseInt(result_page_now, 10)) {
				// 如果当前页在最左按钮所指页面的后面，则修改选中按钮的样式
				$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10) + 1)).css({"border": "1px solid rgba(100, 149, 237, 0.8)"});
				$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10))).css({"border": "3px solid #000"});
				result_page_now = parseInt(result_page_now, 10) - 1;
				// change content
				change_query_result_page();
			} else {
				console.log('pre_page_error!');
				return false;
			}
		}
	});
	
	// 页面跳转按钮-点击事件-下一页
	$('#query_result_page_next').click(function() {
		// 获取当前两边的按钮所指页数
		var left_button = $('#query_result_page_1').val();
		var right_button = $('#query_result_page_10').val();
		var i = 0;
		
		if(!result_page_now || result_page_now <= 0 || result_page_now > result_page_total) {
			console.log('next_page_error! result_page_now is out of range.');
			//alert('next_page_error! result_page_now is out of range.');
			return false;
		} else if(parseInt(result_page_now, 10) === parseInt(result_page_total, 10)) {
			alert('当前页已经是最后一页了');
			return false;
		} else {
			if(right_button.toString() === result_page_now.toString()) {
				// 如果当前页是最右按钮所指的页面，则要调整全部按钮的值
				for(i = 1 ; i <= 10 ; i++) {
					$('#query_result_page_' + i).val( parseInt($('#query_result_page_' + i).val().toString(), 10) + 1 );
				}
				result_page_now = parseInt(result_page_now, 10) + 1;
				// change content
				change_query_result_page();
			} else if(parseInt(right_button, 10) > parseInt(result_page_now, 10)) {
				// 如果当前页在最右按钮所指页面的前面，则修改选中按钮的样式
				$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10) + 1)).css({"border": "1px solid rgba(100, 149, 237, 0.8)"});
				$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10) + 2)).css({"border": "3px solid #000"});
				result_page_now = parseInt(result_page_now, 10) + 1;
				// change content
				change_query_result_page();
			} else {
				console.log('next_page_error!');
				//alert('next_page_error!right_button=' + right_button + '&result_page_now=' + result_page_now);
				return false;
			}
		}
	});
	
	// 页面跳转按钮-点击事件-按按钮跳转
	$('.page_number_button').click(function() {
		// 获取当前两边的按钮所指页数
		var left_button = $('#query_result_page_1').val();
		//var right_button = $('#query_result_page_10').val();
		var button_value = $(this).val();
		
		if(!result_page_now || result_page_now <= 0 || result_page_now > result_page_total) {
			console.log('button_jump_page_error! result_page_now is out of range.');
			return false;
		} else if(!button_value || button_value === "") {
			console.log('button_value is null or ""');
			//alert('button_value is null or ""');
			return false;
		} else if(parseInt(button_value, 10) <= 0 || parseInt(button_value, 10) > parseInt(result_page_total, 10)) {
			alert('搜索结果总共' + result_page_total + '页，请在该范围内查找结果');
			return false;
		} else {
			$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10) + 1)).css({"border": "1px solid rgba(100, 149, 237, 0.8)"});
			$('#query_result_page_' + (parseInt(button_value, 10) - parseInt(left_button, 10) + 1)).css({"border": "3px solid #000"});
			result_page_now = parseInt(button_value, 10);
			// change content
			change_query_result_page();
		}
	});
	
	// 页面跳转按钮-点击事件-按页码跳转
	$('#query_result_page_button').click(function() {
		// 获取当前两边的按钮所指页数
		var left_button = $('#query_result_page_1').val();
		var right_button = $('#query_result_page_10').val();
		var i = 0;
		var page_input = Math.floor( parseInt($('#query_result_page_input').val().toString().trim(), 10) );
		
		if(!result_page_now || result_page_now <= 0 || result_page_now > result_page_total) {
			console.log('input_jump_page_error! result_page_now is out of range.');
			return false;
		} else if(!page_input || page_input === "") {
			alert('请输入合法页码');
			return false;
		} else if(parseInt(page_input, 10) <= 0 || parseInt(page_input, 10) > parseInt(result_page_total, 10)) {
			alert('搜索结果总共' + result_page_total + '页，请输入该范围内的页码');
			return false;
		} else {
			if(parseInt(page_input, 10) < parseInt(left_button, 10)) {
				// 如果输入的页码比最左按钮所指页面的值还小，则调整全部按钮的值，并使最左按钮为选中按钮
				for(i = 1 ; i <= 10 ; i++) {
					$('#query_result_page_' + i).val(parseInt(page_input, 10) + parseInt(i, 10) - 1);
				}
				$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10) + 1)).css({"border": "1px solid rgba(100, 149, 237, 0.8)"});
				$('#query_result_page_1').css({"border": "3px solid #000"});
				result_page_now = parseInt(page_input, 10);
				// change content
				change_query_result_page();
			} else if(parseInt(page_input, 10) > parseInt(right_button, 10)) {
				// 如果输入的页码比最右按钮所指页面的值还大，则调整全部按钮的值，并使最右按钮为选中按钮
				for(i = 10 ; i >= 1 ; i--) {
					$('#query_result_page_' + i).val(parseInt(page_input, 10) + parseInt(i, 10) - 10);
				}
				$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10) + 1)).css({"border": "1px solid rgba(100, 149, 237, 0.8)"});
				$('#query_result_page_10').css({"border": "3px solid #000"});
				result_page_now = parseInt(page_input, 10);
				// change content
				change_query_result_page();
			} else {
				// 如果输入的页码介于最左和最右按钮所指页面的值之间，则只需修改选中按钮的样式
				$('#query_result_page_' + (parseInt(result_page_now, 10) - parseInt(left_button, 10) + 1)).css({"border": "1px solid rgba(100, 149, 237, 0.8)"});
				$('#query_result_page_' + (parseInt(page_input, 10) - parseInt(left_button, 10) + 1)).css({"border": "3px solid #000"});
				result_page_now = parseInt(page_input, 10);
				// change content
				change_query_result_page();
			}
		}
	});
	

	/*
	//切换标签 end
	var user = new document.USER(document.getElementById("userinfo"));
	$.ajax({
		url:"/search/topn/30",
		"type":"GET",
		dataType:"JSON",
		success:function (data) {
			var wordCloudMap = echarts.init(document.getElementById("word-cloud-info"));
			var wordCloudOption ={
				title: {
					text: '搜索热词展示',
					x: 'center',
					textStyle: {
						fontSize: 23
					}
				},
				backgroundColor: '#F7F7F7',
				tooltip: {
					show: true
				},
				toolbox: {
					feature: {
						saveAsImage: {
							iconStyle: {
								normal: {
									color: '#FFFFFF'
								}
							}
						}
					}
				},
				series: [{
					name: '搜索热词展示',
					type: 'wordCloud',
					gridSize: 15,
					sizeRange: [10,40],
					rotationRange: [0, 0],
					shape: 'circle',
					textStyle: {
						normal: {
							color: function() {
								return 'rgb(' + [
										Math.round(Math.random() * 160),
										Math.round(Math.random() * 160),
										Math.round(Math.random() * 160)
									].join(',') + ')';
							}
						},
						emphasis: {
							shadowBlur: 10,
							shadowColor: '#333'
						}
					},
					data: data
				}]
			};
			wordCloudMap.setOption(wordCloudOption);
			$(window).resize(wordCloudMap.resize);
			wordCloudMap.on('click', function (params) {
				//alert((params.name));
				window.open('http://www.kejso.com/search/info?query=' + encodeURIComponent(params.name));
			});
		},
		error:function (e) {
			console.log("加载词云出错！")
		}
	})*/
});