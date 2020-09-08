import traceback
from flask import Flask, render_template, request, redirect, url_for
from dataManager import DataManager
import  datetime
from dbManager import DashboardInfo

OPTIONS = ["ALL_TEST_CASES", "FAILED_IN_CURRENT_RUN", "FAILING_FROM_LAST_10_RUNS", "FAILING_FROM_LAST_3_RUNS", "UNSTABLE_TEST_CASES", "PASS_STATUS_SWITCHED"]

VIEWS=['TABLE_VIEW', 'GRAPH_VIEW']

dataManager= DataManager()


####################### HOME ######################
app = Flask(__name__)

@app.errorhandler(Exception)
def default_error_handler(error):
    '''Default error handler'''
    original = getattr(error, "original_exception", error)
    traceback.print_tb(error.__traceback__)
    print("ERROR occurded during handling message:",original)
    return render_template("view_error.html")

@app.route('/', methods=["GET", "POST"])
def hello():
    all_dashboards = dataManager.get_all_dashboards()
    if request.method == "POST":
        slected_dashboard = request.form['myselect']
        seleted_branch =  request.form['myselect_branch']
        selected_view = request.form['myselect1']
        if  selected_view == 'TABLE_VIEW':
            html = "welcome_table_view.html"
            data = dataManager.get_welcome_table_data(slected_dashboard, seleted_branch)
        else:
            html =  "welcome_new.html"
            data =dataManager.get_welcome_data(slected_dashboard, seleted_branch)
    else:
        slected_dashboard = list(all_dashboards.keys())[0]
        seleted_branch =  all_dashboards[slected_dashboard][0]
        selected_view = VIEWS[0]
        html= "welcome_table_view.html"
        data = dataManager.get_welcome_table_data(slected_dashboard, seleted_branch)

    return render_template(html, data=data,
                           selected_option=slected_dashboard, all_options=all_dashboards.keys(),
                           selected_branch=seleted_branch, all_branches=all_dashboards[slected_dashboard],
                           selected_view=selected_view, all_view_options=VIEWS)

####################### SUIT VIEW ######################
@app.route('/suits/<string:dashboard>/<string:tag>/<string:branch>', methods=["GET", "POST"])
def get_suite(dashboard, tag, branch):
    print("get_suite called with tag = ", dashboard, tag, branch)

    if request.method == "POST":
        return render_template('view_suite_new.html', tag=tag, dashboard=dashboard, branch=branch,
                             all_branches=dataManager.get_all_dashboards()[dashboard], selected_branch=branch,
                             chart_data=[dataManager.get_chart_data(dashboard, tag, branch)],
                             table_data=dataManager.get_suite_table_data(dashboard, tag, branch, request.form['myselect']),
                             selected_option=request.form['myselect'], all_options=OPTIONS)
    else:
        return render_template('view_suite_new.html', tag=tag, dashboard=dashboard,branch=branch,
                             all_branches=dataManager.get_all_dashboards()[dashboard],selected_branch=branch,
                             chart_data=[dataManager.get_chart_data(dashboard, tag, branch)],
                             table_data=dataManager.get_suite_table_data(dashboard, tag, branch, "ALL_TEST_CASES"),
                             selected_option="ALL_TEST_CASES", all_options=OPTIONS)


@app.route('/suits/<string:dashboard>/<string:tag>/compare/<string:branch1>/<string:branch2>/<string:selected_option>', methods=["GET", "POST"])
def get_suite_compare(dashboard, tag, branch1, branch2, selected_option):
    if request.method == "POST":
        selected_option = request.form['myselect']
        selected_dashboard = request.form['myselect_dashboard']
        branch1_new = request.form['myselect_branch_1']
        branch2_new = request.form['myselect_branch_2']
        selected_suit = request.form['myselect_suit']
        if selected_dashboard != dashboard:
            selected_suit = dataManager.get_all_suits(selected_dashboard)[0]
            branch1_new = dataManager.get_all_dashboards()[selected_dashboard][0]
            branch2_new = dataManager.get_all_dashboards()[selected_dashboard][0]
        return redirect(
            url_for('get_suite_compare', dashboard=selected_dashboard, tag=selected_suit, branch1=branch1_new, branch2=branch2_new, selected_option=selected_option))
    else:
        return render_template('view_suite_compare.html', dashboard=dashboard,all_dashboards = dataManager.get_all_dashboards(),
                                all_suits=dataManager.get_all_suits(dashboard), selected_suit=tag,
                               all_branches=dataManager.get_all_dashboards()[dashboard],branch1=branch1,branch2=branch2,
                             table_data=dataManager.get_compare_suite_table_data(dashboard, tag, branch1, branch2, selected_option),
                             selected_option=selected_option, all_options=["ALL_TEST_CASES", "DIFFERENCE", "FAILED_IN_ONE"])

@app.route('/suits/<string:dashboard>/<string:tag>/compare/<string:branch1>/<string:branch2>/<string:branch3>/<string:selected_option>', methods=["GET", "POST"])
def get_suite_3way_compare(dashboard, tag, branch1, branch2, branch3, selected_option):
    if request.method == "POST":
        selected_option = request.form['myselect']
        selected_dashboard = request.form['myselect_dashboard']
        branch1_new = request.form['myselect_branch_1']
        branch2_new = request.form['myselect_branch_2']
        branch3_new = request.form['myselect_branch_3']
        selected_suit = request.form['myselect_suit']
        if selected_dashboard != dashboard:
            selected_suit = dataManager.get_all_suits(selected_dashboard)[0]
            branch1_new = dataManager.get_all_dashboards()[selected_dashboard][0]
            branch2_new = dataManager.get_all_dashboards()[selected_dashboard][0]
            branch3_new = dataManager.get_all_dashboards()[selected_dashboard][0]
        return redirect(
            url_for('get_suite_3way_compare', dashboard=selected_dashboard, tag=selected_suit, branch1=branch1_new, branch2=branch2_new, branch3=branch3_new,
                    selected_option=selected_option))
    else:
        return render_template('view_suite_3way_compare.html', dashboard=dashboard,all_dashboards = dataManager.get_all_dashboards(),
                                all_suits=dataManager.get_all_suits(dashboard), selected_suit=tag,
                               all_branches=dataManager.get_all_dashboards()[dashboard],branch1=branch1,branch2=branch2,branch3=branch3,
                               summary_table_data=dataManager.get_3way_compare_branch_summary(dashboard, tag, branch1,branch2, branch3),
                             table_data=dataManager.get_3way_compare_suite_table_data(dashboard, tag, branch1, branch2, branch3, selected_option),
                             selected_option=selected_option, all_options=["ALL_TEST_CASES", "DIFFERENCE", "FAILED_IN_ONE"])


@app.route('/overview/suits/<string:dashboard>/<string:tag>/<string:branch>', methods=["GET", "POST"])
def get_suite_overview(dashboard, tag, branch):
    print("get_suite called with tag = ", dashboard, tag, branch)
    all_dashboards = dataManager.get_all_dashboards()
    if request.method == "POST":
        print("POST CALL")
        seleted_branch =  request.form['myselect_branch']
        selected_suit = request.form['myselect_suit']
        slected_dashboard = request.form['myselect']
        if slected_dashboard == dashboard:
            #All options are valid
            return redirect(url_for('get_suite_overview', dashboard=slected_dashboard, tag=selected_suit, branch=seleted_branch))
        else:
            # Provide fresh options
            return redirect(url_for('get_suite_overview', dashboard=slected_dashboard, tag=dataManager.get_all_suits(slected_dashboard)[0],
                                    branch=all_dashboards[slected_dashboard][0]))
    else:
        return render_template('view_suite_overview.html', tag=tag, dashboard=dashboard,
                               selected_option=dashboard, all_options=all_dashboards.keys(),
                               all_branches = DashboardInfo.objects(name=dashboard)[0].branches, branch=branch,
                               all_suits=dataManager.get_all_suits(dashboard), selected_suit=tag,
                             chart_data=[dataManager.get_chart_data(dashboard, tag, branch)],
                             table_data=dataManager.get_suite_table_overview_data(dashboard, tag, branch))


####################### COMMIT VIEW ######################
@app.route('/commits/<string:ref_id>')
def commits_ref(ref_id):
    if ref_id =="NA":
        return "<h2>First Build, no previous build to compare with</h2>"
    else:
        notes, ser_com, rest_com, proto_com, node_com, ops_com, udp_com = dataManager.get_commit_ids(ref_id)
        return render_template('view_commit_new.html',
                            notes=notes,
                            build_data=dataManager.get_build_data(ref_id),
                            smf_serice_commit_data= ser_com,
                            smf_restep_commit_data=rest_com,
                            smf_protocol_commit_data=proto_com,
                            smf_nodemgr_commit_data=node_com,
                            smf_opscenter_commit_data=ops_com,
                            smf_udp_proxy_commit_data=udp_com)


####################### TEST VIEW ######################
@app.route('/<string:dashboard>/<string:suit>/<string:unique_name>/<string:branch>')
def get_test_case_data(dashboard, suit, unique_name, branch):
    print(suit, unique_name, branch)
    test_case, data = dataManager.get_test_data(dashboard, suit, unique_name, branch)
    return render_template('view_test_case_new.html', dashboard= dashboard, tag=suit, branch=branch, test_case=test_case,data=data)


####################### CONFIG VIEW ######################
@app.route('/configurations')
def configurations():
    return  render_template('view_configurations.html', dashboard_data=dataManager.get_dashboard_data())


####################### CONFIG VIEW ######################
@app.route('/comapareAny/', methods=["GET", "POST"])
def compareAny():
    if request.method == "POST":
        print (request.form)
        selected_option = request.form['myselect']
        path1 = request.form['path1']
        user1 = request.form['user1']
        pass1 = request.form['pass1']
        tag1 = request.form['tag1'] if request.form['tag1'] != "" else "Tag 1"
        path2 = request.form['path2']
        user2 = request.form['user2']
        pass2 = request.form['pass2']
        tag2 = request.form['tag2'] if request.form['tag2'] != "" else "Tag 2"

        return render_template('view_comapre_any.html', path1=path1, path2=path2,user1=user1, user2=user2, pass1=pass1, pass2=pass2,
                               tag1=tag1, tag2=tag2,
                               all_options=["ALL_TEST_CASES", "DIFFERENCE", "FAILED_IN_ONE"], selected_option = selected_option,
                               table_data=dataManager.GetCompareAnyData(selected_option, path1, path2, user1, user2, pass1, pass2))
    else:
        path1=""
        path2=""
        return render_template('view_comapre_any.html', path1=path1, path2=path2,user1="", user2="", pass1="", pass2="", tag1="Tag 1", tag2="Tag 2",
                               all_options=["ALL_TEST_CASES", "DIFFERENCE", "FAILED_IN_ONE"], selected_option = 'ALL_TEST_CASES',
                               table_data=[])

