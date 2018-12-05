# -*- coding: utf-8 -*-

import re
from illegibility_match import get_school_name

def school_sieve_1(row, pattern_str):
    ret_list = []
    bked = row.find("本科")
    bkst = bked-1
    while(bkst >= 0):
        if(row[bkst].isdigit()):
            break
        bkst = bkst-1
    # print(row[bkst:bked])
    if(bkst >= 0):
        bk_p = re.compile(pattern_str)
        bk_list = bk_p.findall(row[bkst:bked]);
        ret_list.extend(bk_list)

    xsed = row.find("学士")
    xsst = xsed - 1
    # print(xsst)
    while (xsst >= 0):
        if (row[xsst].isdigit()):
            break
        xsst = xsst - 1
    # print(row[xsst:xsed])
    if (xsst >= 0):
        xs_p = re.compile(pattern_str)
        xs_list = xs_p.findall(row[xsst:xsed]);
        ret_list.extend(xs_list)

    ssed = row.find("硕士")
    ssst = ssed - 1
    while (ssst >= 0):
        if (row[ssst].isdigit()):
            break
        ssst = ssst - 1
    if (ssst >= 0):
        ss_p = re.compile(pattern_str)
        ss_list = ss_p.findall(row[ssst:ssed]);
        ret_list.extend(ss_list)

    bsed = row.find("博士")
    bsst = bsed - 1
    while (bsst >= 0):
        if (row[bsst].isdigit()):
            break
        bsst = bsst - 1
    # print(row[bsst:bsed])
    if (bsst >= 0):
        bs_p = re.compile(pattern_str)
        bs_list = bs_p.findall(row[bsst:bsed]);
        ret_list.extend(bs_list)

    return ret_list

def school_sieve_2(row, pattern_str):
    ret_list = []

    byst = row.find("毕业")
    byed = row.find(pattern_str)

    # print(byst)
    # print(byed)

    if(byst < byed and byst != -1 and byed != -1):
        # print(row[byst+3:byed+2])
        flag = True
        for i in range(byst, byed):
            if (row[i] == '；' or
                row[i] == '。' or
                row[i] == '，'):
                flag = False
        if flag == True:
            ret_list.append(row[byst+3:byed+2])

    if(byst > byed and byst != -1 and byed != -1):
        flag = True
        for i in range(byed, byst):
            if (row[i] == '；' or
                row[i] == '。' or
                row[i] == '：' or
                row[i] == ':' or
                row[i] == '，' or
                row[i] == ' '):
                flag = False
            if flag == True:
                pid = byed -1 # 标点符号index
                while(pid >= 0):
                    if (row[pid] == '；' or
                        row[pid] == '。' or
                        row[pid] == '：' or
                        row[pid] == ':' or
                        row[pid] == '，' or
                        row[pid] == ' '):
                        break
                    pid = pid - 1
                if pid >= 0:
                    ret_list.append(row[pid:byed + 2])

    return ret_list

def school_sieve_3(row, pattern_str):
    ret_list = []
    bked = row.find("本科")
    bkst = bked - 1
    while (bkst >= 0):
        if (row[bkst] == '；' or
            row[bkst] == '。' or
            row[bkst] == '：' or
            row[bkst] == ':' or
            row[bkst] == '，' or
            row[bkst] == ' '):
            break
        bkst = bkst - 1
    # print(row[bkst:bked])
    if (bkst >= 0):
        bk_p = re.compile(pattern_str)
        bk_list = bk_p.findall(row[bkst:bked]);
        ret_list.extend(bk_list)

    xsed = row.find("学士")
    xsst = xsed - 1
    # print(xsed)
    while (xsst >= 0):
        if (row[xsst] == '；' or
            row[xsst] == '。' or
            row[xsst] == '：' or
            row[xsst] == ':' or
            row[xsst] == '，' or
            row[xsst] == ' '):
            break
        xsst = xsst - 1
    # print(row[xsst:xsed])
    if (xsst >= 0):
        xs_p = re.compile(pattern_str)
        xs_list = xs_p.findall(row[xsst:xsed]);
        ret_list.extend(xs_list)

    ssed = row.find("硕士")
    ssst = ssed - 1
    while (ssst >= 0):
        if (row[ssst] == '；' or
            row[ssst] == '。' or
            row[ssst] == '：' or
            row[ssst] == ':' or
            row[ssst] == '，' or
            row[ssst] == ' '):
            break
        ssst = ssst - 1
    if (ssst >= 0):
        ss_p = re.compile(pattern_str)
        ss_list = ss_p.findall(row[ssst:ssed]);
        ret_list.extend(ss_list)

    bsed = row.find("博士")
    bsst = bsed - 1
    while (bsst >= 0):
        if (row[bsst] == '；' or
            row[bsst] == '。' or
            row[bsst] == '：' or
            row[bsst] == ':' or
            row[bsst] == '，' or
            row[bsst] == ' '):
            break
        bsst = bsst - 1
    # print(row[bsst:bsed])
    if (bsst >= 0):
        bs_p = re.compile(pattern_str)
        bs_list = bs_p.findall(row[bsst:bsed]);
        ret_list.extend(bs_list)

    return ret_list

def clean_school(row, clp_str):
    dxed = row.find(clp_str)
    dxst = dxed - 1
    while (dxst >= 0):
        if (row[dxst] == '；' or
            row[dxst] == '。' or
            row[dxst] == '：' or
            row[dxst] == ':'  or
            row[dxst] == '，' or
            row[dxst] == ' '):
            break;
        dxst = dxst - 1
    # print(row[dxst+1:dxed+2])
    if (dxst+1 < dxed+2):
        return get_school_name(row[dxst+1:dxed+2])
    else:
        return ''

def school_sieve(row):
    ret_list = []
    pattern_str1 = "[0-9][:：]*[ ]*(.*?大学)"
    pattern_str3 = "[0-9][:：]*[ ]*(.*?学院)"
    pattern_str7 = "[0-9][:：]*[ ]*(.*?专科学校)"

    pattern_str2 = "[；。，][:：]*[ ]*(.*?大学)"
    pattern_str4 = "[；。，][:：]*[ ]*(.*?学院)"
    pattern_str8 = "[；。，][:：]*[ ]*(.*?专科学校)"

    pattern_str5 = "大学"
    pattern_str6 = "学院"
    pattern_str9 = "专科学校"

    ret_list.extend(school_sieve_1(row, pattern_str1))
    ret_list.extend(school_sieve_1(row, pattern_str3))
    ret_list.extend(school_sieve_1(row, pattern_str7))

    ret_list.extend(school_sieve_3(row, pattern_str2))
    ret_list.extend(school_sieve_3(row, pattern_str4))
    ret_list.extend(school_sieve_3(row, pattern_str8))

    ret_list.extend(school_sieve_2(row, pattern_str5))
    ret_list.extend(school_sieve_2(row, pattern_str6))
    ret_list.extend(school_sieve_2(row, pattern_str9))

    cl_ret_list = set()
    clp_str1 = "大学"
    clp_str2 = "学院"
    clp_str3 = "专科学校"
    for ret in ret_list:
        tmp = clean_school(ret, clp_str1)
        if (tmp != None and len(tmp) > 0):
            cl_ret_list.add(tmp)
        tmp = clean_school(ret, clp_str2)
        if (tmp != None and len(tmp) > 0):
            cl_ret_list.add(tmp)
        tmp = clean_school(ret, clp_str3)
        if (tmp != None and len(tmp) > 0):
            cl_ret_list.add(tmp)

    return cl_ret_list

if __name__ == "__main__":
    test1 = "男，1974年4月生，山东高唐人，中共党员，讲师。" \
           "个人简历：1992·9－1996·7 山东大学哲学系本科生" \
           "1996·9－1999·7 山东大学哲学系马克思主义哲学专业硕士生1999·7－2002·8 " \
           "山东聊城大学政法学院哲学教研室教师2002·9－2006·7 北京大学哲学系外国哲学专业博士生 " \
           "2006年8月到人民大学马克思主义学院任教，2006年9月被评为讲师。 " \
           "主要教授课程： 马克思主义基本原理概论、思想道德修养与法律基础、哲学专业外语、西方哲学基本问题研究。 " \
           "研究方向： 国外马克思主义、比较哲学 科研项目： 人民大学2006年度科研基金项目：“国外马克思主义对现代性的态度”。" \
           "主要科研成果（2006年以来）：“中国古代哲理思想的诗化表达”，《烟台大学学报》2007年第1期 " \
           "联系方式：E-mail: zhangxiaohua1974@sina.com"
    test2 = "1963年2月出生，湖北黄冈人，博士，教授。2002年毕业于华中科技大学，获博士学位。" \
            "主要研究方向：化工多相流和反应器技术，溶剂萃取和超临界萃取技术，腐蚀电化学和化工环保。" \
            "曾从事化工部科技攻关项目胶磷矿充填浮选柱的研制，" \
            "以化学反应工程、质量传递理论为基础，完成了气液固三相流体流动模型的验证和P2O5的柱式分选工作。" \
            "应用充填气浮装置，完成了超细粉体SiO2的表面改性和纯化、造纸废水和淀粉废水应用技术的开发。" \
            "从腐蚀电化学原理出发，借助于AAS、 SEM、XPS、SPM（AFM）等测试手段，" \
            "对强腐蚀性有机介质乳酸材质进行了评价和分析，并从氧质量传递过程的观点，以含硅湿法磷酸为研究体系，" \
            "导出了液固两相流湍流腐蚀的作用区域模型，该模型对流动诱导的电化学腐蚀控制具有现实的意义。" \
            "采用络合萃取完成了乙二醛溶液中回收稀醋酸的研究，并从乙二醛路线出发，合成了精细产品尿囊素。" \
            "采用溶剂萃取法完成了从茶叶末中分离抗氧化剂茶多酚工艺及动力学研究。应用超临界CO2流体技术，" \
            "完成了超临界CO2萃取甜橙皮油的工艺研究、从GBE中提取银杏内酯类的工艺研究，并对超临界精制乳酸钙等工作开展了研究。" \
            "联系方式： 电话：027-87195671，13627298248电子邮件：ygding@public.wh.hb.cn"
    test3 = "1959?1964：哈尔滨工业大学精密仪器专业学习，本科毕业； " \
            "1964?1978：哈尔滨工业大学精密仪器系任教； " \
            "1978?1988：哈尔滨工业大学精密仪器系讲师； " \
            "1988?1993：哈尔滨工业大学精密仪器系副教授； " \
            "1993?2000：哈尔滨工业大学自动化测试与控制系教授； " \
            "2000?目前：哈尔滨工业大学自动化测试与控制系博士生导师"
    test4 = "基本信息姓名：丁晟春性别:女 出生年月:1971-3职称:副教授 " \
            "最后学历:硕士 所学专业:信息管理 " \
            "毕业院校:南京理工大学 籍贯:江苏政治面貌:其他 " \
            "学术信息 研究方向:企业信息管理系统的设计与开发 数据库应用 " \
            "主讲课程:数据库原理及应用计算机网络基础 web程序设计电子商务网站的设计与管理 " \
            "参与项目:WWW网站设计与开发 主要著作:《电子商务网站设计与管理》获奖情况:" \
            "联系方式办公电话:84315963 E-mail:todingding@163.com"
    test5 = "万力所在单位：中国地质大学(北京) 水资源与环境学院" \
            "通讯地址：北京市学院路29号邮 编：100083电 话：+86-10 - 8232 7933传 真：+86-10 - 8232 1081" \
            "E-mail: wanli@cugb.edu.cn学历" \
            "1978～1982年，南京大学，理学学士，水文地质及工程地质专业" \
            "1982～1985年，中国地质大学(北京)，工学硕士，水文地质专业，电网络模拟研究方向" \
            "1985～1988年，中国地质大学(北京)，工学博士，水文地质专业，裂隙水渗流研究方向经历" \
            "1988.07～1990.10,中国地质大学(北京)，讲师" \
            "1990.10～1992.10,中国地质大学(北京)，副教授" \
            "1992.10～至今, 中国地质大学(北京)，教授" \
            "2001.01～2001.5,荷兰IHE学院和Wangeningen大学合作研究（中荷西北地下水开发合作项目）" \
            "2003.12～2004.4,荷兰Wangeningen大学合作研究（荷兰农业部IAC基金资助）" \
            "2006.01～2006.4,美国Alabama大学合作研究（Drummond访问教授）兼职中国地质大学（北京）" \
            "水资源与环境学院院长国务院学位委员会环境科学与工程学科评议组成员中国建筑学会工程勘察专业委员会常务委员中国地质学会环境地质专业委员会委" \
            "中国地质学会水文地质专业委员会委员中国地质学会西部工作委员会委员中国地质调查局城市环境地质研究中心学术委员会委员" \
            "国际水文地质学家协会中国国家委员会副主席国防科工委高放废物地质处置专家组成员" \
            "“水文地质工程地质”编委“工程勘察”编委“地学前缘”编委“现代地质”编委 奖励" \
            "1990年，国家教委和国务院学位委员会授予“做出突出贡献的中国博士学位获得者”称号" \
            "1993年，北京市高教局评为“北京市高等学校优秀青年学术带头人”1993年，国务院授予“政府特殊津贴”" \
            "1995年，中国地质学会授予“银锤奖”1989年，获地矿部科技进步三等奖1991年，获地矿部科技进步三等奖" \
            "1991年，获水利部黄河水利委员会科技进步一等奖1992年，获水利部科技进步二等奖" \
            "2003年，获国土资源部科技进步二等奖2006年，获国土资源部科技进步二等奖"
    test6 = "万志强，男，1976年11月出生，汉族，江西省南昌市人，博士，飞行器设计专业副教授，硕士生导师。 2003年11月博士毕业于北京航空航天大学航空科学与工程学院。2005年12月从北航流体力学博士后流动站出站后留校工作。现任北航航空创新实践基地副主任。2005年度获国防科学技术奖三等奖一项。2005年被评为北航优秀博士后。2006年获北航“蓝天新秀”称号。主要研究领域为飞行器设计领域的气动弹性、飞行器总体设计、飞行器结构设计，研究对象包括固定翼飞机、微小型飞行器等。主持或参加科研课题近10项，包括自然基金、预研以及多个型号的科研课题。在微小型飞行器设计、飞行载荷、颤振、气动弹性优化、复合材料气动弹性剪裁方面有多年的理论和实践，发表重要期刊论文10余篇。多年担任北航航模队指导教师组组长，所指导学生连续四年获得全国航空航天模型锦标赛载重飞行项目个人冠军、团体冠军并创造全国纪录；多年担任学生科技辅导老师，指导多名学生多次获得校“冯如杯”奖励及全国“挑战杯”奖励。联系方式：010-82317510，82316034；E-mail：wzq@buaa.edu.cn通讯地址：北京航空航天大学飞机所，100083"
    test7 = "1977年5月生，福建泉州人。北京外国语大学亚非系泰语专业学士；北京大学外语学院东语系泰国语言文化硕士；北京大学国际关系学院国际政治系在读博士研究生。主要研究方向：1、泰国政治2、泰国非政府组织研究3、泰国语言文化"
    test8 = "上官文慧：性别：女 民族：满族 政治面貌：中共党员专业：经济学学历：经济学硕士毕业学校：中央民族大学经济学院工作经历：1990年7月毕业至今一直在教学第一线从事教学工作，先后讲授了“马克思主义政治经济学原理”、“中国社会主义建设”、“邓小平理论”、“国际贸易”、“中国税制”、“国民经济管理”、“当代世界经济与政治”等课程。教育教学成果： 主持了2003－2004年校“马克思主义政治经济学原理”课合格课建设。论文“关于马克思主义政治经济学原理课教学方法的调查与分析”2005年《黑龙江民族丛刊》专刊。论文“课程建设是加强思想政治理论课教学的关键——从‘马克思主义政治经济学原理’课合格课建设想到的”2006年《黑龙江民族丛刊》专刊。"
    test9 = "上官铁梁 男，汉族，1955年5月生，山西阳城人，教授，研究生导师。中共党员，1978年毕业于山西大学生物系植物生理专业，曾任山西省科学技术协会第五届委员，山西大学生物系植物教研室主任，生命科学系副主任，山西大学环境与资源学院环境工程系主任。现任山西大学教学指导委员会委员，山西大学环境与资源学院教授治院委员会主任。兼任山西省植物学会理事长、山西省生态学会常务理事、山西省野生动物保护协会常务理事、山西省教授协会理事、山西省五台山研究会理事、山西省生态经济学会理事。获国家清洁生产审计师和国家环境评价资职证书。论文名称.1.山西五台山地区大型真菌调查报告2.一个未开发的天然草坡3.黑蛋巢菌属的一个新种4.山茱萸的生物学生态学特性及在我省的发展概况5.山西主要植被类型及其分布的初步研究6.山西绵山植被的模糊图论分类研究7.山西省东北部植被的研究8.关于晋西北部森林与森林草原的界线及森林草原带的划分9.山西南方红豆杉森林群落的生态优势度10.山西绵山植被优势种群的分布格局与种间联结的研究11.柠条林地水分动态研究12.山西植被的水平地带性分析13.云顶山虎榛子灌丛群落学特征及生物量14.荆条的核型分析15.朔县植被及其保护利用改造对策16.胡秃子属二种植物的核型研究17.云顶山植被及其垂直分布研究18.太原地区植物区系的初步研究19.关帝山黄刺玫灌丛群落结构与生物量的研究20.山西朔县种子植物区系及其生态经济意义21.模糊图论在山西植被区划中的应用22.山西关帝山华北落叶松的生物量23.山西云蒙山油松种群的年龄结构和动态特征24.山西翅果油树灌丛的生态地理分布和群落学特征25.关帝山华北落叶松的群落学特征和生物量26.太岳山种子植物区系的初步研究27.关于灌丛生物量建模方法的改进28.山西9种野生植物的染色体观察29.山西蜜源植物花粉的数量分类研究30.山西蟒河自然保护区鹅耳枥林的聚类和排序31.翅果油树群落的数量分类32.山西蟒河自然保护区栓皮栎林的聚类和排序33.逐步聚类法及其应用34.山西高原植被与气候的关系分析及植被数量区划的研究35.山西草地资源及合理利用36.山西香料植物资源及其特点评价37.山西沙棘灌丛的群落特征及其合理利用38.On the numerical classification regionalizationof Shanxi，North China39.山西雪花山野生植物资源研究40.有序样聚类在植被垂直带划分中的应用41.山西木本植物区系地理成分的比较分析42.中条山植被垂直带谱再分析43.山西省珍稀濒危植物及其保护对策研究44.A comparison of three methods of veget ationanalysis exemplified by investigation of the Elaeagnus mollis community of Shanxi，North China45.The vertical belts of natural vegetation partitioning of the Guandi Mountains by using ordered plot clustering，Shanxi，North China46.五台山亚高山草甸小格局分析47.五台山亚高山草甸群落生态关系分析48.A study on flora of woody plants of Shanxi and the relationship among the flora of Shanxiand some regions， China49.山西关帝山种子植物区系研究50.山西太岳山野生植物资源研究51.山西湿地植物资源研究52.濒危植物矮牡丹种群生物量的研究53.山西绵山森林植被的多样性分析54.濒危植物矮牡丹的分布格局及其生存群落的数量分类55.汾河河岸植被类型及其利用与保护56.滹沱河湿地假苇拂子茅群落生物量调查57.山西高原植被与土壤分布格局关系的研究58.平原型灰场植物群落多样性研究59.汾河流域娄烦县植被类型及其利用保护对策研究60.山西湿地生物多样性及其保护61.山西湿地资源及可持续利用研究62.芦芽山自然保护区种子植物区系地理成分分析63.山西翅果油树群落的多样性研究64.趋势面分析及其在山西省沙棘灌丛水平格局分析中的应用65.中条山木本植物区系地理成分分析.66.山西湿地维管植物区系多样性研究.67.汾河河漫滩草地植物群落的分类及多样性分析.68.芦芽山自然保护区野生植物资源.69.中国大气污染的研究现状和对策.70.晋西山地植物区系多样性研究.71.晋西王家沟流域植被及其保护利用.72.山西关帝山神尾沟植物群落多样性研究.73.山西翅果油树群落种间关系的数量分析.74.芦芽山植物群落的多样性研究75.植物群落永久样方数据演替分析方法----类中心排序法76.山西翅果油树群落优势种群分布格局研究77.汾河河漫滩三种草本植物群落的生物量研究78.滹沱河湿地狭叶香蒲群落生物量研究79.濒危植物矮牡丹无性系分株种群的结构80.我国特有珍稀植物翅果油树濒危原因分析81.滹沱河流域湿地植被类型及保护利用对策82.珍稀濒危植物矮牡丹体内矿质元素的研究83.山西省湿地的基本特征及保护84.四种早春植物生物量的动态研究85.恒山种子植物区系地理成分分析86.汾河太原段河漫滩草地植被的数量分类与排序87.太原市清洁生产评价指标体系研究88.汾河河漫滩野生植物资源研究89.矮牡丹体内无机元素分布规律的研究90.汾河太原段河漫滩草地土壤种子库研究91.神头二电厂灰场植物群落分析研究92.历山自然保护区猪尾沟森林群落多样性研究93.芦芽山自然保护区旅游开发与植被环境的关系1. 植被环境质量分析94.山西东南部白羊草群落植物种多样性研究95.滹沱河湿地植物群落的种间关系研究96.芦芽山自然保护区旅游开发与植被环境的关系—旅游影响系数及指标体系97.汾河河漫滩草地种子植物多样性及其保护对策 98.山西翅果油树资源及可持续利用研究99.黄河中游（禹门口～桃花峪）河漫滩种子植物区系地理研究100.突出山西自身优势，促进旅游业发展101.太原市清洁生产评价指标体系之一——城市生态建设评价指标体系102.太岳山森林群落物种多样性103.太岳山森林群落优势种群生态位研究104.山西北部地区沙棘群落的数量分类和排序研究 105.山西省种子植物多样性分布格局与环境关系的研究106.历山山地草甸的物种多样性及其与土壤理化性质的关系107.黄河中游师弟资源湿地资源及其可持续利用108.滹沱河流域湿地植被的数量分类与排序109.山西省稷山和永济两地区矮牡丹体内化学元素特征的比较110.拧条锦鸡儿不同居群形态变异研究111.生态学概论 112.生态学概论 113.太原植物志 114.太原植被 115.生态学概论 116.山西省珍稀濒危保护植物 117.山西植被 118.应用生态学 119.应用生态学"
    test10 = "丛培田，男，教授，机械工程分院副院长，清华大学硕士毕业，硕士生导师。现从事机械制造、自动化，振动测试及仪表专业。科研方向： 现场动平衡测试仪器的制造；旧式动平衡机的微机化改造；振动测量及仪器；机械设计与制造。工作优势： 本科毕业于清华大学，学习机械制造专业，硕士研究生毕业于清华大学，学习精密仪器专业，因此机械、电子及其微机知识融会贯通，善于解决机电结合的问题。自从1988年以来，一直坚持科研工作和教学工作，对企业有广泛的接触和深刻的了解，并且在长期的科研工作中积累了丰富的经验。现在负责分院的科研工作，在分院组织了4个科研梯队，具有科研攻关能力，有能力接受各种难题。科研成果及荣誉：IMB-2智能化多功能动平衡仪或省级科研成果；一种动平衡仪和一种角度测试仪获实用型专利；完成了27吨风机转子动平衡机、9吨动平衡机微机化的改造以及3KG动平衡机的制造；曾被授予沈阳理工大学十佳科技青年和先进科技工作者荣誉称号。"
    test11 = "姓名 丰雷 (男) 职称或学历学位 副教授,管理学博士。中国土地学会青年工作委员会理事。土地估价师。 主要研究方向 不动产经济、城市经济、不动产制度与政策分析、房地产市场调查与分析、计量经济学等。 主要学术作品 出版学术著作7部，在《管理世界》、《中国土地科学》、《光明日报（理论版）》等期刊上发表学术论文数十篇，主持国家自然科学基金、教育部人文社科项目各1项，参加国家自然科学基金、国家社科基金、教育部等国家级、省部级科研课题10余项。 教育背景与社会学术兼职 1991-1995年中国人民大学统计学系，统计学本科；1995-1998年中国人民大学土地管理系，房地产经营管理硕士；1998-2000年中国人民大学农业经济系，土地经济博士；2000-今，任教于中国人民大学土地管理系。2006-2007年在剑桥大学土地经济系作访问学者主要讲授课程：土地经济学、房地产经济学、城市经济学、计量经济学在房地产研究中的应用等。 主持的主要科研课题 联系方式 通信地址：中国人民大学土地管理系（100872）电话：82502296（办）；13911850322E-mail：flfl@sina.com 或 fenglei@mparuc.edu.cn"
    test12 = "姓名：乐善堂 男 博士 教授 联系方式： 华南师范大学化学与环境学院 电话：13711179206 Email：yuest@scnu.edu.cn 学习及工作经历：2001~现在 华南师范大学化学与环境学院1998~2001 中国科学院长春应用化学研究所1991~1998 湖北师范学院化学系1989~1991 中国地质大学应用化学系1986~1989 中国科学院长春应用化学研究所 TOP讲授课程：无机化学 无机与分析化学 新材料概论 纳米材料导论 稀土化学 高等无机化学无机化学实验 TOP研究领域和学术兴趣：⑴ 金属有机骨架配合物⑵ 多孔气体吸附材料⑶ 无机分离TOP近年研究课题：⑴ 广东省自然科学基金, 项目编号: 7005808, 项目经费: 5万元, 主持⑵ 广州市荔湾区科技攻关基金, 项目编号: 20072108076, 项目经费: 20万元, 主持⑶ 国家基金委广东省联合基金, 目编号: U0734005, 项目经费: 150万元, 合作⑷ 湖北省自然科学基金（1996），主持⑸ 参与研究课题: 稀土功能材料的基础研究G1998061302，G1998061301（国家973项目）、国家自然科学基金2971028，29801004TOP成果及获奖：1998年“稀土及相关金属离子溶剂萃取化学基础研究”获中国科学院自然科学二等奖，本人完成其中“稀土溶剂萃取动力学研究”部分，主要参与者。发表论文40余篇。 TOP代表性论文和论著(按时间倒序)：1. Su-Li Xie, Bi-Qin Xie, Xiao-Yong Tang, Ning Wang, and Shan-Tang Yue*, Hydrothermal Synthesis, Structures and Thermal Stability of Two Novel Lanthanide Complexes: [Er4(tp)6(H2O)6], [Lu(tp)1.5(H2O)3], Z. Anorg. Allg. Chem., 2008, 634(5):842~8442. Ning Wang, Shan-Tang Yue*, and Ying-Liang Liu，One 2-D 3d-4f Heterometallic Compound: Hydrothermal Synthesis, Structure and Magnetic Properties，Z. Anorg. Allg. Chem., 2008, 6343. Tang X.Y., Yue S.T*., Hydrothermal synthesis and crystal structure study of two novel 3-D mellitates {Nd2[C6(COO)6](H2O)6} and {Ho2[C6(COO)6](H2O)6}, Chin. J. Rare Earths, 20084. Ping Li, Yongcai Qiu, Jianqiang Liu, Yun Ling, Yuepeng Cai, Shantang Yue*. Puckered-boat conformation (H2O)14 cluster on the self-assembly of an inorganic-metal-architecture. Inorg. Chem. Commun., 2007, 10:705~7085. Ping Li, Xiao-Yong Tang, Rong-Hua Zeng and Shan-Tang Yue*. 1,10-Phenanthrolinium 2,4,5- tricarboxybenzoate. Acta Cryst. 2007, E63:0448~04496. Xiao-Yong Tang, Yong-Cai Qiu, Feng Sun and Shan-Tang Yue*, Diaquabis(1,10-phenanthro -line-k2N,N’)nickel(II) diperchlorate 0.4-hydrate, Acta Cryst. 2007, E63: m25157. Yue shantang, Li Deqian, Su Qiang. Extraction Kinetics of Rare Earth Elements with sec-Octylphenoxy Acetic Acid. Chin. J. Chem., 2002, 21(6):545~5498. Yue Shantang, Liao Wuping, Li Deqian, Su Qiang. Extraction Mechanism of Rare Earths with Sec-Octylphenoxy Acetic Acid by Two-Phase Titration Technique. Chin. J. Rare Earths, 2002, 20(5):416~4199. Wang Y.G., Yue S.T., Li D.Q. Kinetics and mechanism of Y(III) extraction with CA-100 using a constant interfacial cell with laminar flow. Solv. Extra. Ion Exch., 2002, 20(3):345~35810. Wang Y. G., Yue S.T., Li D.Q., Jin M. J., Li C.Z. Solvent extracion of scandium(Ⅲ), yttrium(Ⅲ), lanthanides(Ⅲ), and divalent metal ions with sec-nonylphenoxy acetic acid. Solv. Extra. Ion Exch., 2002, 22(6):701~71611. Wuping Liao, Guihong Yu, Shantang Yue, Deqian Li. Kinetics of Cerium(IV) Extraction from H2SO4--HF Medium with Cyanex923. Talanta, 2002, 56:613~61812. Yu Guihong, Yue Shantang, Li Deqian. Kinetic study of Ce4+ extraction with Cyanex923. Chin. J. Rare Earths, 2001, 19(4):250~25413. 乐善堂, 王艳枝，李德谦，苏锵. 仲辛基苯氧基乙酸基本常数的测定.分析化学, 2001, 29 (8): 954~95614. 姚有为, 赵永男, 乐善堂, 一种新型杂化单晶[Ga3(PO4)3F2]H2O×(H3NCH2)2NH2的合成与结构表征. 高等学校化学学报, 2001, 22(9):1450~145215. 乐善堂, 马根祥, 李德谦, 苏锵. 铒在HBTMPTP-正庚烷/水溶液间的传质动力学.高等学校化学学报, 2000, 21(6):832~835会议论文：1. Ping Li, Xiao-Yong Tang,Rong-Hua Zeng and Shan-TangYue，Hydrothermal synthesis, Crystal structure and Characterization of a novel Dysprosium complex of phthalic acid and 1,10-phenanthroline，第五届国际稀土开发与应用研讨会暨第五届国际稀土学术会议, 内蒙古, 2007.8.2. Tang Xiaoyong，Li Ping，Yue Shangtang，Hydrothemal synthesis and crystals tructure studio of two novel 3-D mellitates {Nd2[C6(COO)6] (H2O)6}and {Ho2[C6(COO)6](H2O)6}，第五届国际稀土开发与应用研讨会暨第五届国际稀土学术会议, 内蒙古, 2007.8.3. X.Y. Tang, N. Wang, H.Y. Wu, S.T. Yue. Hydrothermal Synthesis and Characterization of Two Novelo 3-D Lanthanide Mellitates Complexes, 中国化学会第五届全国结构化学学术会议, 福州, 2007.10.4. N. Wang, X.Y. Tang, S.T. Yue. Synthesis and Characterization of Two Lanthanide-oxalate- pyridine- dicarboxylate Cordination Polymers, 中国化学会第五届全国结构化学学术会议, 福州, 2007.10.5. X.Y. Tang, S.T. Yue. Hydrothermal Synthesis and Characterization of a Tetranuclear Erbium(III) Complex with One-dimensional, 中国化学会第五届全国结构化学学术会议, 福州, 2007.10.6. YUE Shan-Tang, LI De-Qian, SU Qiang. Kinetics of rare earth extraction with sec- octylphenoxy acetic acid. ISEC’2002"
    test13 = "1967年出生，分别于1988年和1991年在浙江大学获理学学士学位和理学硕士学位。1991年4月起在西安建筑科技大学工作，1997年7月调至西安交通大学工作。2004年在北京化工大学获工学博士学位。现在北京化工大学教育部超重力工程研究中心工作，主要从事纳米材料和纳米药物的制备方法研究、纳米粒子的表面修饰技术开发、性能测试及应用开发等方面的研究。参加过国家攻关项目、973、863等项目的研究工作。近年来在“J. Non-Crystalline Solids”、“Applied Surf. Sci.”等国际国内期刊上发表学术论文30多篇"
    test14 = "乐艳芬 上海财经大学会计学院副教授，硕士生导师，上海财经大学精品课程《成本会计》负责人 上海市成本研究会理事，上海市《成本研究》副主编教育经历： 上海财经大学管理学硕士，上海财经大学经济学学士 讲授课程： 成本会计、管理会计、战略成本管理、CGA专业课程Management Accounting、财务会计、管理会计研究、财务会计研究 研究领域： 成本管理会计出国经历： 2005年9月至2006年12月,加拿大University of British Columbia(UBC)学习主要研究成果： 主编的教材及专著： 1、《成本会计》，2007年8月，上海财经大学出版社2、《战略成本管理与企业竞争优势》，2006年8月，复旦大学出版社3、《成本会计》，2005年7月，清华大学出版社 4、《成本管理会计》 ，2005年3月，中国财政经济出版社 5、《管理会计》，2004年8月，上海财经大学出版社 6、《管理会计》，2003年2月，立信会计出版社? 7、《成本会计》，2002年1月，上海财经大学出版社 8、《管理会计》，2000年7月，高等教育出版社、上海社会科学院联合出版 9、《经营决策会计》，1996年1月，航空出版社出版 10、《投资决策会计》，1996年1月，航空出版社出版 11、《当代中国经济大辞库》保险会计分篇，1993年12月，中国经济出版社出版 论文：1、《目标成本管理在汽车零部件行业应用研究》，郑州航空工业管理学报，2008年第3期2、《整合的成本管理系统和价值链分析》，四川会计，2003年第11期 3、《新制造环境和成本管理》，四川会计，2002年第12期 4、《成本会计课程建初探》，财经高教研究，2002年第3期 5、《质量成本：现代企业面临的新挑战》，工业会计，2002年第3期 6、《无形成本动因和企业竞争优势》，上海会计，2000年第7期 7、《战略成本管理和战略定位》，财会研究，2000年第2期 8、《现代成本管理与决策机制》，财经研究，1999年第5期 9、《试谈现代企业成本管理的变革》，上海会计，1999年第2期 10、《析现金折扣总价之不足》，上海会计，1998年第7期 11、《合并报表的权益法和成本法》，财会通讯，1996年第11期12、《制造费用的分配方法》，财会通讯，1993年第9期 主持的课题：《战略成本管理与竞争优势》，上海财经大学211课题。 《上海电信成本优化》，横向课题。 联系方式 yueyf@mail.shufe.edu.cnyueyf666@163.com"
    test15 = "乔兰 性别 女 出生年月 1963年10月 技术职称 教授 行政职务 发展规划与学科建设办公室主任 所在学院 土木与环境工程学院 招生专业 岩土工程 联系电话 010-62334012 E-mail lanqiao@pgschl.ustb.edu.cn 研究方向 1、工程地质灾害机理分析与控制技术2、地应力测量理论与技术3、特殊土地基处理及其稳定性研究4、工程岩土体稳定性及其环境效应毕业院校信息： 2000年6月毕业于北京科技大学工程力学专业，获博士学位 1983年7月毕业于华北水利水电学院工程地质、水文地质专业并获学士学位，1993年获得北京科技大学采矿工程专业硕士学位，2000年获得北京科技大学工程力学专业博士学位； 1983-1990在华北水利水电学院地质系工程地质教研室任教，1993年始进入北京科技大学，至今历任土木与环境工程学院副研究员、教授、博士生导师，曾任土木工程系副主任、主任、研究生院副院长等职务，现任北京科技大学规划与学科建设办公室主任，兼任中国岩石力学与工程学会理事、中国岩石力学与工程学会测试专委会副主任委员。 主要从事岩土工程、工程力学和采矿工程等领域的“工程岩土体稳定性分析与控制技术”、“地应力测试技术理论与方法”、“工程地质灾害机理分析与控制技术”、“特殊土地基处理技术”方面的科学研究与研究生教育工作。 作为主要研究骨干或项目负责人参与完成了国家“八.五”、“九.五”、“十.五”等重点科技攻关课题4项，国家自然科学基金课题2项，省部级项目10余项。高等学校博士点基金项目3项，教育部优秀青年教师资助项目1项，以及20余项校企合作科研课题。其中包括峨口铁矿、金川镍矿、梅山铁矿、新城金矿、玲珑金矿、海沟金矿、首钢水厂铁矿等多个矿山地下巷道和高陡边坡的岩体稳定性控制技术研究项目，以及京秦高速公路青龙连接线岩质边坡稳定性控制、京承高速公路长大隧道超前地质预报及稳定性控制技术等项目，在岩土工程监测理论和技术、工程地质及其环境效应、地应力测试技术理论与方法、采空区处理、GIS与矿山安全生产等方面积累了丰富的研究经验。研究成果曾获得国家科技进步二等奖2项，国家技术发明三等奖1项，省部级科技进步特等奖2项、一等奖4项。第二届中国岩石力学与工程学会青年科技奖金奖。出版了二部学术专著和一部教材，在《岩石力学与工程学报》、《中国矿业》、《金属矿山》等国内外学术期刊发表论文40余篇（其中被SCI、EI收录论文21篇）。在教学方面：独立指导10届硕士生21名、指导已毕业博士研究生3名；指导的硕士毕业生论文有2篇获得北京科技大学优秀硕士学位论文。主讲了包括《土力学地基基础》、《工程地质学》、《地质力学》、《地下水动力学》及《高等土力学》、《工程地质分析原理》在内的多门本科生和研究生主干课程。培养毕业博士2人、硕士9人（其中2名硕士优秀硕士学位论文）和在读博士生8人、硕士生12人。"


    # ttest = "业，获博士学位 1983年7月毕业于华北水利水电学院工程地质、水文地质专业并获学士学位，199"
    #
    # tmp = school_sieve(ttest)
    # print(tmp)

    tmp = school_sieve(test1)
    print(tmp)
    tmp = school_sieve(test2)
    print(tmp)
    tmp = school_sieve(test3)
    print(tmp)
    tmp = school_sieve(test4)
    print(tmp)
    tmp = school_sieve(test5)
    print(tmp)
    tmp = school_sieve(test6)
    print(tmp)
    tmp = school_sieve(test7)
    print(tmp)
    tmp = school_sieve(test8)
    print(tmp)
    tmp = school_sieve(test9)
    print(tmp)
    tmp = school_sieve(test10)
    print(tmp)
    tmp = school_sieve(test11)
    print(tmp)
    tmp = school_sieve(test12)
    print(tmp)
    tmp = school_sieve(test13)
    print(tmp)
    tmp = school_sieve(test14)
    print(tmp)
    tmp = school_sieve(test15)
    print(tmp)
