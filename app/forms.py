from flask_wtf import FlaskForm

from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import (StringField, BooleanField, FloatField,
                     IntegerField, SubmitField,
                     TextAreaField, PasswordField, SelectField, SelectMultipleField,
                     DecimalField, RadioField)

from wtforms.validators import DataRequired, Email, EqualTo, Required, ValidationError


from wtforms.fields.html5 import DateField

from .models import User


# Login Form
class LoginForm(FlaskForm):

    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')



# Registration Form
class RegistrationForm(FlaskForm):

    username = StringField(u'用户名', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    password2 = PasswordField(
        u'重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(u'注册账号')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(u'用户名已存在')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(u'邮件地址已存在')


# Add Dish Form
class AddDishForm(FlaskForm):

    name = StringField(u"菜品名称", validators=[DataRequired()])
    class_name = SelectField('菜品类型',
                             choices=[("Please select", u"请选择菜品类型")],
                             validators=[DataRequired()])

    category = SelectField(u"菜品种类",
                           choices=[("Please select", u"请选择菜品种类")],
                           validators=[DataRequired()])

    description = TextAreaField(u"菜品描述", validators=[DataRequired()])
    price = FloatField(u"单价", validators=[DataRequired()])
    image = FileField(u"上传图片", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    eat_manner = SelectField(u"用餐方式", choices=[("Please select", u"请选择用餐方式"),
                                                ("Buffet", u"自助餐"),
                                               ("takeaway", u"外卖"),
                                               ("AlaKarte", u"单点")])
    submit = SubmitField(u"确认添加")


class EditCategoryForm(FlaskForm):

    name_class = SelectField(u"菜品类型",
                             choices=[("Please select", u"请选择菜品类型")])

    new_class = StringField(u"添加新类型")

    name_category = SelectField(u"菜品种类",
                                choices=[("Please select", u"请选择菜品种类")])

    new_category = StringField(u"添加新种类")

    unit_en = StringField(u"计量单位 zh")

    submit = SubmitField(u"确定修改")


class AddCategoryForm(FlaskForm):

    name_class = SelectField(u"菜品类型",
                             choices=[("Please select", u"请选择菜品类型")])

    new_class = StringField(u"添加新类型")

    name_category = SelectField(u"菜品种类",
                                choices=[("Please select", u"请选择菜品种类")])

    new_category = StringField(u"添加新种类")

    unit_en = StringField(u"计量单位 zh")

    submit = SubmitField(u"确定添加")


# Edit Dish Form
class EditDishForm(FlaskForm):

    name = StringField(u"菜品名称", validators=[DataRequired()])
    class_name = SelectField('菜品类型',
                             choices=[("Please select", u"请选择菜品类型")],
                             validators=[DataRequired()])

    category = SelectField(u"菜品种类",
                           choices=[("Please select", u"请选择菜品种类")],
                           validators=[DataRequired()])

    description = TextAreaField(u"菜品描述", validators=[DataRequired()])
    price = FloatField(u"单价", validators=[DataRequired()])
    image = FileField(u"上传图片", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    eat_manner = SelectField(u"用餐方式", choices=[("Please select", u"请选择用餐方式"),
                                               ("Buffet", u"自助餐"),
                                               ("takeaway", u"外卖"),
                                               ("AlaKarte", u"单点")])
    submit = SubmitField(u"确认更新")


# Store Settings Form
class StoreSettingForm(FlaskForm):

    store_name = StringField(u"餐馆名称", validators=[DataRequired()])
    city = StringField(u"城市", validators=[DataRequired()])
    street = StringField(u"街道名称", validators=[DataRequired()])
    street_no = StringField(u"街道号码", validators=[DataRequired()])
    country = StringField(u"所在国", validators=[DataRequired()])
    zip = StringField(u"邮编", validators=[DataRequired()])
    tax_id = StringField(u"税号", validators=[DataRequired()])
    tax_rate_takeaway = FloatField(u"外卖", validators=[DataRequired()])
    tax_rate_InHouse = FloatField(u"在店", validators=[DataRequired()])
    logo = FileField(u"LOGO", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField(u"确认更新")


class CheckoutForm(FlaskForm):

    payment = SelectField(u'支付方式', choices=[("-","-"),("Cash","Cash"), ("Card", "Card")])
    coupon_amount = FloatField(u"代金券€")
    discount_rate = FloatField(u"打折")
    subtotal = DecimalField("Subtotal")
    tax = FloatField("Tax")
    grandtotal = FloatField("Grandtotal")
    card_submit = SubmitField(u"卡帐")
    cash_submit = SubmitField(u"现金")


class AddTableForm(FlaskForm):

    name = StringField(u"桌子名称", validators=[DataRequired()])

    persons = IntegerField(u"桌子人数", validators=[DataRequired()])

    section = SelectField(u'桌子分区',
                          choices=[("Please select section", u"请选择分区")],
                          validators=[DataRequired()])

    submit = SubmitField(u"确认添加")


class EditTableForm(FlaskForm):

    name = StringField(u"桌子名称", validators=[DataRequired()])

    persons = IntegerField(u"桌子人数", validators=[DataRequired()])

    section = SelectField(u'桌子分区',
                          choices=[("Please select section", u"请选择分区")],
                          validators=[DataRequired()])

    submit = SubmitField(u"确认更新")


class ConfirmForm(FlaskForm):

    submit = SubmitField("确定")


class TableSectionQueryForm(FlaskForm):

    start_section = SelectField(u'开始',
                          choices=[("Please select section", u"请选择开始分区")],
                          validators=[DataRequired()])

    end_section = SelectField(u'结束',
                                choices=[("Please select section", u"请选择结束分区")],
                                validators=[DataRequired()])

    submit = SubmitField(u"确认")


class SearchTableForm(FlaskForm):

    select_table = SelectField(u'搜索桌号',
                        choices=[("Please select section", u"请选择桌子号码")],
                        validators=[DataRequired()])

    submit = SubmitField(u"搜索")


class TransferTableForm(FlaskForm):

    cur_table = StringField(u'当前桌子', validators=[DataRequired()])

    target_table = SelectField(u'目标桌子',
                                choices=[("Please select section", u"请选择转至桌子")],
                                validators=[DataRequired()])

    submit = SubmitField(u"确认转台")


class DatePickForm(FlaskForm):

    start_date = DateField(u'开始日期', validators=[DataRequired()])

    end_date = DateField(u'截止日期', validators=[DataRequired()])

    submit = SubmitField(u'搜索')


# Registration Form
class AddUserForm(FlaskForm):

    username = StringField(u'用户名', validators=[DataRequired()])
    alias = StringField(u'姓名', validators=[DataRequired()])

    permissions = SelectField(u'设置权限',
                             choices=[(2, u"等级2 - 管理员"),
                                      (3, u"等级3 - 超级管理员（可访问老板页面）")],
                             validators=[DataRequired()])

    account_type = SelectField(u'设置账户类型',
                             choices=[(0, u"外卖"),
                                      (1, u"跑堂")],
                             validators=[DataRequired()])

    section = SelectMultipleField(u'负责分区',
                                choices=[],
                                validators=[DataRequired()])

    password = PasswordField(u'设置密码', validators=[DataRequired()])
    password2 = PasswordField(
        u'重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(u'添加')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(u'用户名已存在')


# Edit User Form
class EditUserForm(FlaskForm):

    username = StringField(u'用户名', validators=[DataRequired()])
    alias = StringField(u'姓名', validators=[DataRequired()])

    section = SelectMultipleField(u'负责分区',
                                  choices=[],
                                  validators=[DataRequired()])

    permissions = SelectField(u'设置权限',
                              choices=[(2, u"等级2 - 管理员"),
                                       (3, u"等级3 - 超级管理员（可访问老板页面）")],
                              validators=[DataRequired()])

    account_type = SelectField(u'设置账户类型',
                               choices=[(0, u"外卖"),
                                        (1, u"跑堂")],
                               validators=[DataRequired()])

    password = PasswordField(u'设置密码', validators=[DataRequired()])
    password2 = PasswordField(
        u'重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(u'更新')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(u'用户名已存在')


class EditPrinterForm(FlaskForm):

    terminal = StringField(u"终端名称", validators=[DataRequired()])

    printer = StringField(u'打印机名称', validators=[DataRequired()])

    submit = SubmitField(u"确认更新")

