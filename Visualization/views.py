from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http.response import Http404, JsonResponse, HttpResponse
from django.db.models import Q
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime
import operator

from .models import BasicInfo, AcademicInfo, PaperInfo


def basicinfo_2_json(obj):
    return {
        "id": obj.id,
        "name": obj.name,
        "university": obj.university,
        "college": obj.college,
        "theme_list": obj.theme_list,
        "sub_list": obj.sub_list,
        "resume": obj.resume,
        "img_url": obj.img_url,
        "url1": obj.url1,
        "url2": obj.url2
    }


def toDict(obj):
    return dict([(attr, getattr(obj, attr)) for attr in [f.name for f in obj._meta.fields]]) # type(self._meta.fields).__name__


def sort_experts(all_experts):
    experts = []
    result = []
    for expert in all_experts:
        acadamic_info = AcademicInfo.objects.get(id=expert.id)
        score = acadamic_info.h_index * acadamic_info.amount2 / acadamic_info.amount1
        tup = (expert, score)
        experts.append(tup)

    tmp = sorted(experts, key=lambda expert : expert[1], reverse=True)
    for ele in tmp:
        result.append(json.dumps(toDict(ele[0])))
        # print('学者排名得分：' + str(ele[1]))

    return result


# 专家列表展示
class ExpertListView(View):
    def get(self, request):

        # all_experts = BasicInfo.objects.all()[:10]

        query_type = request.GET.get("query_type", "")
        query_selection = request.GET.get("query_selection", "")
        query_input = request.GET.get("query_input", "")
        researcher = request.GET.get("researcher_input", "")
        field = request.GET.get("field_input", "")
        research_content = request.GET.get("research_content_input", "")
        organization = request.GET.get("organization_input", "")

        # print(query_input)
        # all_experts = BasicInfo.objects.all()[:10]

        # print(query_type)

        print(query_type, query_input, query_selection)
        if query_type == "normal":

            # TODO 这里使用的SQL中用到了LIKE ‘%%’ 将导致放弃索引，使用全表扫描，如何优化？ 配置全文检索
            if query_selection == "researcher":
                all_experts = BasicInfo.objects.filter(name__icontains=query_input)
            elif query_selection == "field":
                all_experts = BasicInfo.objects.filter(theme_list__icontains=query_input)
            elif query_selection == "research_content":
                all_experts = BasicInfo.objects.filter(sub_list__icontains=query_input)
            elif query_selection == "organization":
                all_experts = BasicInfo.objects.filter(university__icontains=query_input)
            else:
                raise Http404

        elif query_type == "advanced":
            # TODO 改用intersection操作，避免where子句中用and操作，使用qs1 = intersection(qs2,qs3)
            if(len(researcher) != 0):
                experts1 = BasicInfo.objects.filter(name__icontains=researcher)
            else:
                experts1 = BasicInfo.objects.all()
            if(len(field) != 0):
                experts2 = BasicInfo.objects.filter(theme_list__icontains=field)
            else:
                experts2 = BasicInfo.objects.all()
            if (len(research_content) != 0):
                experts3 = BasicInfo.objects.filter(sub_list__icontains=research_content)
            else:
                experts3 = BasicInfo.objects.all()
            if (len(organization) != 0):
                experts4 = BasicInfo.objects.filter(university__icontains=organization)
            else:
                experts4 = BasicInfo.objects.all()
            # experts2 = BasicInfo.objects.filter(name__icontains=field)
            # experts3 = BasicInfo.objects.filter(name__icontains=research_content)
            # experts4 = BasicInfo.objects.filter(name__icontains=organization)
            #
            all_experts = experts1 & experts2 & experts3 & experts4

            # all_experts = BasicInfo.objects.filter(Q(name__icontains=researcher),
            #                                        Q(theme_list__icontains=field),
            #                                        Q(sub_list__icontains=research_content),
            #                                        Q(university__icontains=organization))


        else:
            raise Http404

        # return render_to_response("list.html", {"all_experts": all_experts, })
        # return render_to_response("index.html", {"all_experts": serializers.serialize("json", all_experts),})
        result = sort_experts(all_experts)
        # all_experts_list = list(all_experts)
        # for expert in all_experts:
        #     result.append(json.dumps(toDict(expert)))

        # json.dumps(result)
        # print(json.dumps(result))
        if request.is_ajax():
            print("ajax访问", len(result))
            # print(result)
            # return HttpResponse(serializers.serialize("json", all_experts), content_type='application/json')
            # return render_to_response("index.html", {"all_experts": serializers.serialize("json", list(all_experts)),})
            return HttpResponse(json.dumps(result))
        else:
            return render_to_response("index.html")

    # return JsonResponse(serializers.serialize("json", all_experts), safe=False)

    def post(self, request):
        query_type = request.POST.get("query_type", "")
        query_selection = request.POST.get("query_selection", "")
        query_input = request.POST.get("query_input", "")
        researcher = request.POST.get("researcher_input", "")
        field = request.POST.get("field_input", "")
        research_content = request.POST.get("research_content_input", "")
        organization = request.POST.get("organization_input", "")

        # all_experts = BasicInfo.objects.all()[:10]

        # print(query_type)

        if query_type == "normal":
            if query_selection == "researcher":
                all_experts = BasicInfo.objects.filter(name__icontains=query_input)
            elif query_selection == "field":
                all_experts = BasicInfo.objects.filter(theme_list__icontains=query_input)
            elif query_selection == "research_content":
                all_experts = BasicInfo.objects.filter(sub_list__icontains=query_input)
            elif query_selection == "organization":
                all_experts = BasicInfo.objects.filter(university__icontains=query_input)
            else:
                raise Http404

        elif query_type == "advanced":
            # TODO 查询优化
            all_experts = BasicInfo.objects.filter(Q(name__icontains=researcher),
                                               Q(theme_list__icontains=field),
                                               Q(sub_list__icontains=research_content),
                                               Q(university__icontains=organization))

        else:
            raise Http404

        # return render_to_response("index.html", {"all_experts": json.dumps(list(all_experts)), })
        if request.is_ajax():
            # print("ajax访问")
            return HttpResponse(serializers.serialize("json", all_experts), content_type='application/json')
        else:
            return render_to_response("index.html", {"all_experts": serializers.serialize("json", all_experts), })


# 专家详情展示
class ExpertDetailView(View):
    def get(self, request):
        expert_id = request.GET.get("id", "")
        expert_basic = BasicInfo.objects.get(id=expert_id)
        print(expert_basic)

        expert_academic = AcademicInfo.objects.get(id=expert_id)

        # papers = PaperInfo.objects.filter(author1=expert_id)

        # papers = PaperInfo.objects.filter(Q(authors__icontains=expert_basic.name),
        #                                   Q(author1=expert_id) |
        #                                   Q(author2=expert_id) |
        #                                   Q(author3=expert_id) |
        #                                   Q(author4=expert_id) |
        #                                   Q(author5=expert_id))

        date1 = datetime.now()
        papers1 = PaperInfo.objects.filter(author1=expert_id)
        papers2 = PaperInfo.objects.filter(author2=expert_id)
        papers3 = PaperInfo.objects.filter(author3=expert_id)
        papers4 = PaperInfo.objects.filter(author4=expert_id)
        papers5 = PaperInfo.objects.filter(author5=expert_id)
        date2 = datetime.now()

        print(".........查询花费时间：" + str((date2-date1).seconds))

        papers = papers1 | papers2 | papers3 | papers4 | papers5

        paper_list = []
        for paper in papers:
            paper_list.append(json.dumps(toDict(paper)))

        co_experts_id = []
        for co_expert_id in expert_academic.co_expert[1:-1].replace(' ', '').split(','):
            co_experts_id.append(co_expert_id[1:-1])

        co_experts_info = []
        for co_expert_id in co_experts_id:
            print(co_expert_id)
            try:
                basic_info = BasicInfo.objects.get(id=co_expert_id)
                dicts = {
                    "id": co_expert_id,
                    "name": basic_info.name,
                    "resume": basic_info.resume,
                    "img_url": basic_info.img_url,
                }
                co_experts_info.append(json.dumps(dicts))
            except :
                print("数据库中无此学者id:" + co_expert_id + "对应的信息")
                pass

        # print(co_experts_info)

        result = {
            "expert_basic": json.dumps(toDict(expert_basic)),
            "expert_academic": json.dumps(toDict(expert_academic)),
            "papers": json.dumps(paper_list),
            "co_experts_info": json.dumps(co_experts_info)
        }

        # print(result)
        if request.is_ajax():
            print("ajax访问 detail page", len(result))
            return HttpResponse(json.dumps(result))
        else:
            print("非ajax访问")
            return render_to_response("detail.html")
        # return render(request, "detail.html", result)

    def post(self):
        pass
