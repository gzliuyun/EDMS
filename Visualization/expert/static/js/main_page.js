// JavaScript Document

/* jshint esversion: 6 */

function query_http(qi, qt, qs, r, f, rc, org){
	'use strict';
	//var server_url = "http://localhost/expert/researcher_list";
	var server_url = "{% url 'expert:list' %}";
	if(qt === "normal") {
/*		qt = encodeURIComponent(qt);
		if(qi && qi !== "") {
			qi = encodeURIComponent(qi);
		} else {
			return false;
		}
		if(qs && qs !== "") {
			qs = encodeURIComponent(qs);
		} else {
			return false;
		}

		location.href = server_url + "?" +
			"query_input=" + qi +
			"&query_type=" + qt +
			"&query_selection=" + qs;
		*/
		/*
		server_url = server_url + "?" +
			"query_input=" + qi +
			"&query_type=" + qt +
			"&query_selection=" + qs;
		*/
		/**/
		// HTTP GET (JQuery Ajax)
		$.ajax({
			type: "GET",
			url: server_url,
			data: {
				"query_input": qi,
				"query_type": qt,
				"query_selection": qs
			},
			dataType: "json",
			beforeSend: function(xhr) {
				//
				//alert('HTTP GET BeforeSend! xhr=' + xhr.val());
				//alert('HTTP GET BeforeSend.');
				alert('server_url= ' + server_url);
			},
			success: function(result, status, xhr) {
				// 清空query_result_list里面的所有内容
				$('#query_result_list').empty();
				// 对返回结果的每个元素，增添到html_template里
				var html_template = '<div class="researcher_result_name">';
				$.each(result, function(index, value) {
					html_template += '<p>' + index + ': ' + value.name + ':</p>';
				});
				html_template += '</div>';
				// 增添子元素到query_result_list结点
				$('#query_result_list').html(html_template);
				//
				//alert('HTTP GET Success! result=' + result.val() + '&status=' + status.val() + '&xhr=' + xhr.val());
				alert('HTTP GET Success! result=' + result.val() + '&status=' + status.val());
			},
			error: function(xhr, status, error) {
				//
				//alert('HTTP GET Error! xhr=' + xhr.val() + '&status=' + status.val() + '&error=' + error.val());
				alert('HTTP GET Error!');
			},
			statusCode: {
				// 当响应对应的状态码时，执行对应的回调函数
				200: function() {
					alert("请求成功");
				},
				404: function(){
					alert("找不到页面");
				},
				500: function() {
					alert( "服务器错误" );
				}
			},
		});

//		$.get("localhost:8000/expert/list", {
//				"query_input": qi,
//				"query_type": qt,
//				"query_selection": qs
//			}, function(result) {
//			    // 清空query_result_list里面的所有内容
//				$('#query_result_list').empty();
//				// 对返回结果的每个元素，增添到html_template里
//				var html_template = '<div class="researcher_result_name">';
//				$.each(result, function(index, value) {
//					html_template += '<p>' + index + ': ' + value.name + ':</p>';
//				});
//				html_template += '</div>';
//				// 增添子元素到query_result_list结点
//				$('#query_result_list').html(html_template);
//				//
//				//alert('HTTP GET Success! result=' + result.val() + '&status=' + status.val() + '&xhr=' + xhr.val());
//				alert('HTTP GET Success! result=' + result.val() + '&status=' + status.val());
//		});
		alert('normal_query_http: send ok');
	} else if(qt === "advanced") {
		qt = encodeURIComponent(qt);
		if(r && r !== "") {
			r = encodeURIComponent(r);
		}
		if(f && f !== "") {
			f = encodeURIComponent(f);
		}
		if(rc && rc !== "") {
			rc = encodeURIComponent(rc);
		}
		if(org && org !== "") {
			org = encodeURIComponent(org);
		}
		location.href = server_url + "?" +
			"query_type=" + qt +
			"&researcher_input=" + r +
			"&field_input=" + f +
			"&research_content_input=" + rc +
			"&organization_input=" + org;
		alert('advanced_query_http: send ok');
	} else {
		return false;
	}
}

// 输入控制
function query_function() {
	'use strict';
	var query_type = $("#query_type").val().trim();
	
	if(query_type === "normal") {
		alert('query_function() query_input=' + query_input +
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
		alert('query_function() query_type=' + query_type +
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

/*
function myCountUp(target,startnum,endnum,decimals,duration){
	'use strict';
	var options = {
		useEasing : true,
		useGrouping : true,
		separator : ',',
		decimal : '.',
		suffix: " +",
	};
	var myCountUp = new CountUp(target, startnum, endnum, decimals, duration, options);
	myCountUp.start();
}
*/

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
	//myCountUp("peopleNum",100000,2000000,0,1);
	//myCountUp("fieldNum",10000000,100000000,0,1);
	//myCountUp("orgNum",0,50000,0,1);

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
	$('#query_selection_list ul li').click(function(){
		$(this).addClass('active').siblings().removeClass('active');
	});

	$('#researcher').click(function(){
		$('#researcher_word').addClass('active');
		$('#field_word').removeClass('active');
		$("#query_selection").val("researcher");
	});

	$('#field').click(function(){
		$('#researcher_word').removeClass('active');
		$('#field_word').addClass('active');
		$("#query_selection").val("field");
	});
	
	$('#research_content').click(function(){
		$('#researcher_word').removeClass('active');
		$('#field_word').removeClass('active');
		$("#query_selection").val("research_content");
	});

	$('#organization').click(function(){
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
	
	
	//
	$('#testa').click(function() {
		alert('jumping');
        //根据a标签的href转换为id选择器，获取id元素所处的位置，并高度减50px（这里根据需要自由设置）
        $('html,body').animate(
			{
				scrollTop: ($($(this).attr('href')).offset().top - 50 )
			}, 1000
		);
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