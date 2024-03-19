from flask_web import admin, root, api
from flask_admin import BaseView, expose
from flask import abort, flash, redirect, render_template, request, url_for
import requests as rq


class AnalyticsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/analytics_index.html")


class UserView(BaseView):
    @expose("/")
    def user(self):
        id_param = request.args.get("id")
        if not id_param:
            flash("User ID is required", "error")
            return self.render("admin/user.html", error={"message": "User not found"})
        info = api.get_user_by_id(id_param)
        if info:
            return self.render("admin/user.html", info=info)
        return self.render("admin/user.html", error={"message": "User not found"})


class UserSurveyView(BaseView):
    @expose("/")
    def user_survey(self):
        id_param = request.args.get("id")
        if not id_param:
            flash("User ID is required", "error")
            return self.render("admin/user_survey.html", error={"message": "User not found"})
        info = api.get_surveys_by_user_id(id_param)
        print(info)
        if info:
            return self.render("admin/user_survey.html", info=info)
        return self.render("admin/user_survey.html", error={"message": "User not found"})


admin.add_view(AnalyticsView(name="Accounts", endpoint="analytics"))
admin.add_view(UserView(name="User", endpoint="user"))
admin.add_view(UserSurveyView(name="Survey", endpoint="user_surveys/"))
