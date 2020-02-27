# _*_coding:utf8_*_
# Project: lin_mass_tools
# File: window.py
# Author: ClassmateLin
# Email: 406728295@qq.com
# Time: 2020/2/23 7:53 上午
# DESC:
import os
import sys
import random
import time
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFileDialog
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QTextBrowser
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget, QApplication
from PyQt5.QtCore import pyqtSignal
import threading
import queue
from app.background import get_backgound
from app.article import CSDNArticle
from app.proxy import QuickProxy, XunProxy
from app.visitor import RequestVisitor

PROXY_LIST = ['免费代理', '讯代理(付费)']
VISIT_MODEL = ['无界面访问', '浏览器访问(需安装驱动)']

PROXY_TITLE_MAP = {
    0: '免费代理',
    1: '讯代理(付费)'
}

PROXY_CLASS_MAP = {
    0: QuickProxy,
    1: XunProxy
}


MESSAGE_TITLE = '提示'    # 消息框标题

LABEL_STYLE_SHEET = "QLabel{border:2px groove gray;border-radius:10px;padding:2px 4px;color:black;}"
START_BUTTON_STYLE_SHEET = "QPushButton{border:2px groove gray;border-radius:10px;padding:2px 4px;color:green;}"
PROXY_BUTTON_STYLE_SHEET = "QPushButton{border:2px groove gray;border-radius:10px;padding:2px 4px;color:black;}"
STOP_BUTTON_STYLE_SHEET = "QPushButton{border:2px groove gray;border-radius:10px;padding:2px 4px;color:yellow;}"
IMPORT_BUTTON_STYLE_SHEET = "QPushButton{border:2px groove gray;border-radius:10px;padding:2px 4px;color:blue;}"
DESTROY_BUTTON_STYLE_SHEET = "QPushButton{border:2px groove gray;border-radius:10px;padding:2px 4px;color:red;}"
TEXT_BROWSER_STYLE_SHEET = "QTextBrowser{border:2px groove gray;border-radius:10px;padding:2px 4px;color:black;}"
TABLE_STYLE_SHEET = "QTableWidget{border:2px groove gray;border-radius:10px;padding:2px 4px;color:black;}"
LINE_EDIT_STYLE_SHEET = "QLineEdit{border:2px groove gray;border-radius:10px;padding:2px 4px;}"
WIDGET_STYLE_SHEET = "QWidget{color:gray;}"
TITLE_STYLE_SHEET = "QLabel{padding:2px 4px;color:black;}"
CHECK_BOX_SHEET = "QComboBox{border:2px groove gray;border-radius:10px;padding:2px 4px;color:black;}"


class Window(QWidget):
    """
    窗体
    """
    table_read_num_signal = pyqtSignal(dict)  # 阅读数更新信号
    log_text_signal = pyqtSignal(str)

    def __init__(self):
        """
        初始化窗体
        """
        super().__init__()
        self.w_layout = None

        self._start_btn = None   # 开始按钮
        self._stop_btn = None    # 结束按钮
        self._destroy_btn = None   # 退出按钮
        self._proxy_btn = None  # 获取代理

        self._blog_name_input = None  # 博客名称输入
        self._thread_num_input = None   # 线程数输入
        self._while_num_input = None    # 轮数输入
        self._visit_space_input = None  # 访问间隔输入
        self._import_proxy_btn = None

        self._articles_table = None     # 文章表格
        self._log_text_browser = None   # 文本显示

        self._order_no = None
        self._secret = None

        self._proxy_input = None
        self._proxy_check_box = None
        self._visit_model_check_box = None

        self.setStyleSheet(WIDGET_STYLE_SHEET)
        self.resize(800, 600)

        self.setup_ui()  # 设置控件

        self._init_log_text()
        self._start_btn.clicked.connect(self.start)  # 开始
        self._stop_btn.clicked.connect(self.stop)  # 终止
        self._destroy_btn.clicked.connect(self.destroy)  # 退出
        self._proxy_btn.clicked.connect(self._on_get_proxy)  # 获取代理
        self._import_proxy_btn.clicked.connect(self.import_proxy)  # 导入代理

        self._is_start = False  # 标志是否已经开始
        self._running = True   # 标识是否运行改为, False子线程会退出

        self.table_read_num_signal.connect(self._update_table_read_num)
        self.log_text_signal.connect(self._show_to_log)

        self._proxies = queue.Queue()
        self._lock = threading.Lock()
        self.setMinimumSize(600, 500)

        self._articles = []

    def _on_get_proxy(self):
        """
        获取代理按钮曹函数
        :return:
        """
        self.log_text_signal.emit('正在获取代理')
        page = int(self._proxy_input.text())
        proxy_obj = QuickProxy(page)
        proxies = proxy_obj.get_all()
        random.shuffle(proxies)
        print(proxies)
        for pro in proxies:
            self._proxies.put(pro)
            self.log_text_signal.emit('代理:{}'.format(pro))
        self.log_text_signal.emit('获取免费代理完成...')

    def center(self):
        """
        窗口居中
        :return:
        """
        # 获得窗口
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setup_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.w_layout = QVBoxLayout()  # 全局布局采用垂直布局

        h_layout1 = QHBoxLayout()

        blog_name_label = QLabel('博客名称')
        blog_name_label.setStyleSheet(LABEL_STYLE_SHEET)

        thread_num_label = QLabel('线程数')
        thread_num_label.setStyleSheet(LABEL_STYLE_SHEET)

        while_num_label = QLabel('访问轮数')
        while_num_label.setStyleSheet(LABEL_STYLE_SHEET)

        visit_space_label = QLabel('访问间隔')
        visit_space_label.setStyleSheet(LABEL_STYLE_SHEET)

        self._blog_name_input = QLineEdit('ClassmateLin', minimumWidth=100)  # 博客名称输入框
        self._blog_name_input.setStyleSheet(LINE_EDIT_STYLE_SHEET)

        self._thread_num_input = QLineEdit('5', minimumWidth=2)    # 线程数量输入框
        self._thread_num_input.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        self._thread_num_input.setMaxLength(2)
        thread_num_validator = QIntValidator(self._blog_name_input)
        thread_num_validator.setRange(1, 99)
        self._thread_num_input.setValidator(thread_num_validator)

        self._while_num_input = QLineEdit('5', minimumWidth=5)     # 访问轮数输入框
        self._while_num_input.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        self._while_num_input.setMaxLength(6)
        while_num_validator = QIntValidator(self._while_num_input)
        while_num_validator.setRange(1, 65535)
        self._while_num_input.setValidator(while_num_validator)

        self._visit_space_input = QLineEdit('1', minimumWidth=2)   # 访问间隔秒
        self._visit_space_input.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        visit_space_validator = QIntValidator(self._visit_space_input)
        visit_space_validator.setRange(1, 60)
        self._visit_space_input.setValidator(visit_space_validator)
        self._visit_space_input.setMaxLength(2)

        h_layout2 = QHBoxLayout()

        proxy_label = QLabel('代理页数')
        proxy_label.setStyleSheet(LABEL_STYLE_SHEET)
        self._proxy_input = QLineEdit('5', minimumWidth=2)
        self._proxy_input.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        proxy_validator = QIntValidator()
        proxy_validator.setRange(1, 99)
        self._proxy_input.setValidator(proxy_validator)
        self._proxy_btn = QPushButton('获取代理')
        self._proxy_btn.setStyleSheet(PROXY_BUTTON_STYLE_SHEET)

        self._proxy_check_box = QComboBox()
        self._proxy_check_box.addItems(PROXY_LIST)
        self._proxy_check_box.setStyleSheet(CHECK_BOX_SHEET)

        self._visit_model_check_box = QComboBox()
        self._visit_model_check_box.addItems(VISIT_MODEL)
        self._visit_model_check_box.setStyleSheet(CHECK_BOX_SHEET)

        self._start_btn = QPushButton('开始')   # 开始刷访问量按钮
        self._start_btn.setStyleSheet(START_BUTTON_STYLE_SHEET)

        self._stop_btn = QPushButton('停止')    # 停止刷访问量按钮
        self._stop_btn.setStyleSheet(STOP_BUTTON_STYLE_SHEET)

        self._destroy_btn = QPushButton('退出')
        self._destroy_btn.setStyleSheet(DESTROY_BUTTON_STYLE_SHEET)

        h_layout1.addWidget(blog_name_label)
        h_layout1.addWidget(self._blog_name_input)

        h_layout1.addWidget(thread_num_label)
        h_layout1.addWidget(self._thread_num_input)

        h_layout1.addWidget(while_num_label)
        h_layout1.addWidget(self._while_num_input)

        h_layout1.addWidget(visit_space_label)
        h_layout1.addWidget(self._visit_space_input)

        h_layout2.addWidget(proxy_label)
        h_layout2.addWidget(self._proxy_input)
        h_layout2.addWidget(self._proxy_check_box)
        h_layout2.addWidget(self._proxy_btn)
        h_layout2.addWidget(self._visit_model_check_box)
        h_layout2.addWidget(self._start_btn)
        h_layout2.addWidget(self._stop_btn)
        h_layout2.addWidget(self._destroy_btn)

        h_widget1 = QWidget()
        h_widget1.setLayout(h_layout1)

        h_widget2 = QWidget()
        h_widget2.setLayout(h_layout2)

        h_widget3 = QWidget()
        h_layout3 = QHBoxLayout()
        h_widget3.setLayout(h_layout3)

        order_label = QLabel('讯代理订单号')
        order_label.setStyleSheet(LABEL_STYLE_SHEET)
        h_layout3.addWidget(order_label)

        self._order_no = QLineEdit('ZFxxx')
        self._order_no.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        h_layout3.addWidget(self._order_no)

        secret_label = QLabel('讯代理秘钥')
        secret_label.setStyleSheet(LABEL_STYLE_SHEET)
        h_layout3.addWidget(secret_label)

        self._secret = QLineEdit('absfasaxxxx')
        self._secret.setStyleSheet(LINE_EDIT_STYLE_SHEET)
        h_layout3.addWidget(self._secret)

        self._import_proxy_btn = QPushButton('文件导入代理')
        self._import_proxy_btn.setStyleSheet(IMPORT_BUTTON_STYLE_SHEET)
        h_layout3.addWidget(self._import_proxy_btn)

        v_layout = QVBoxLayout()

        v_widget = QWidget()
        v_widget.setLayout(v_layout)

        self._articles_table = QTableWidget()
        self._articles_table.setStyleSheet(TABLE_STYLE_SHEET)
        self._articles_table.setWindowTitle('文章列表')
        self._articles_table.setColumnCount(3)
        self._articles_table.setRowCount(0)
        self._articles_table.setHorizontalHeaderLabels(['文章标题', '文章链接', '阅读数量'])
        font = self._articles_table.horizontalHeader().font()
        font.setBold(True)
        self._articles_table.horizontalHeader().setFont(font)
        self._articles_table.setSelectionBehavior(QAbstractItemView.SelectItems)
        self._articles_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        articles_label = QLabel('文章列表')
        articles_label.setStyleSheet(TITLE_STYLE_SHEET)
        articles_label.setAlignment(QtCore.Qt.AlignCenter)

        log_text_label = QLabel('日志记录')
        log_text_label.setStyleSheet(TITLE_STYLE_SHEET)
        log_text_label.setAlignment(QtCore.Qt.AlignCenter)

        self._log_text_browser = QTextBrowser()
        font = QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self._log_text_browser.setFont(font)
        self._log_text_browser.setStyleSheet(TEXT_BROWSER_STYLE_SHEET)

        v_layout.addWidget(articles_label)
        v_layout.addWidget(self._articles_table)
        v_layout.addWidget(log_text_label)
        v_layout.addWidget(self._log_text_browser)
        self.w_layout.addWidget(h_widget1)
        self.w_layout.addWidget(h_widget2)
        self.w_layout.addWidget(h_widget3)
        self.w_layout.addWidget(v_widget)

        self.setLayout(self.w_layout)

        palette = QtGui.QPalette()
        self.setWindowOpacity(0.99)
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(get_backgound())))
        self.setPalette(palette)

    def _init_log_text(self):
        text = """ 
                        <<使用说明>>
/**************************************************************************************************
|          博客名称输入你的博客名称, 如你的博客主页地址为https://blog.csdn.net/ClassmateLin/,            
|        那么ClassmateLin就是需要输入的博客名称。                                                      
|          线程数量多有助于提升效率, 过多会导致电脑卡顿。                                                
|          访问轮数表示: 访问所有文章的次数，有些文章会随机跳过或多访问几次，提高真实性。                     
|          访问间隔表示: 访问完一篇文章，隔多久访问下一篇文章。                   
|          需要先获取代理，或者从文件导入代理, 然后点开始运行。详情见https://github.com/ClassmateLin/csdn-increment-visitor。
|          实现原理见博文: https://blog.csdn.net/ClassmateLin/article/details/104423904       
****************************************************************************************************/
        """
        self._log_text_browser.append(text)

    def start(self):
        """
        :return:
        """
        if self._is_start:
            QMessageBox.information(self, MESSAGE_TITLE, '程序已在运行！', QMessageBox.Yes)
            return

        self._is_start = True
        self._running = True
        self.get_articles_and_show_to_table()

        articles = self._articles

        thread_num = int(self._thread_num_input.text())

        if self._proxy_check_box.currentIndex() == 1:  # 付费代理
            order_no = self._order_no.text()
            secret = self._secret.text()

            pro = XunProxy(order_no=order_no, secret=secret)
            self.log_text_signal.emit('使用付费动态ip代理...')
            for i in range(thread_num):
                threading.Thread(target=self.dynamic_proxies_visit, args=(articles, pro.proxy, pro.headers)).start()
        else:
            if self._proxies.qsize() == 0:
                QMessageBox.information(self, MESSAGE_TITLE, '使用免费代理请先获取代理或导入代理！', QMessageBox.Yes)
                self._is_start = False
                self._running = False
                self.log_text_signal.emit('未获取/导入代理, 程序启动失败!')
                return
            for i in range(thread_num):
                threading.Thread(target=self._visit, args=(articles,)).start()
        self.log_text_signal.emit('开启{}个线程, 开始刷访问量!'.format(str(thread_num)))

    def get_articles_and_show_to_table(self):
        """
        获取文章并显示到窗体
        :return:
        """
        for rowNum in range(0, self._articles_table.rowCount())[::-1]:  # 逆序删除，正序删除会有一些删除不成功
            self._articles_table.removeRow(rowNum)
        self._log_text_browser.append('正在获取博客文章列表...')
        self._articles = self._get_articles()
        self._show_article_to_table(self._articles)
        self._log_text_browser.append('获取博客文章完成...')

    def _get_articles(self):
        """
        获取博客文章
        :return:
        """
        blog_name = self._blog_name_input.text().strip()
        art_obj = CSDNArticle(blog_name)
        articles = art_obj.get_all()
        return articles

    def _visit(self, articles):
        """
        访问文章
        :param articles:
        :return:
        """
        while_num = int(self._while_num_input.text())
        count = 0
        while self._running and count < while_num:
            self._visit_single(articles)
            count += 1
        self._running = False
        self._is_start = False

    def dynamic_proxies_visit(self, articles, proxy, headers):
        """
        动态代理访问
        :param articles
        :param proxy:
        :param headers:
        :return:
        """
        visitor = RequestVisitor()
        while self._running:
            for i in range(len(articles)):
                if not self._running:
                    self.log_text_signal.emit('停止线程:{}...'.format(str(threading.currentThread().ident)))
                    self._is_start = False
                    return
                is_visit = random.choice([True, False])
                if is_visit:
                    raw_read_num = int(self._articles_table.item(i, 2).text())  # 文章列表显示的访问量
                    read_num = visitor.visit(articles[i]['url'], proxy, headers)
                    if read_num == 0:
                        self.log_text_signal.emit('代理连接失败...')
                        continue
                    self.update_table_view(articles, i, read_num, raw_read_num)
        self._is_start = False
        self.log_text_signal.emit('停止线程:{}, 任务已完成...'.format(str(threading.currentThread().ident)))

    def update_table_view(self, articles, i, read_num, raw_read_num):
        """
        更新视图
        :param articles:
        :param i:
        :param read_num:
        :param raw_read_num:
        :return:
        """
        if read_num == 0:  # 表示访问失败
            self.log_text_signal.emit('文章:{}, 代理访问超时...'.format(articles[i]['title']))
            return
        if read_num == raw_read_num:  # 重复IP在60秒内访问同一篇文章不会增加访问量
            self.log_text_signal.emit('文章:{}, 访问量增加失败...'.format(articles[i]['title']))
            return
        log_text = '文章:{}访问量+1, 当前访问量:{}。'.format(articles[i]['title'], str(read_num))
        self.log_text_signal.emit(log_text)

        self.table_read_num_signal.emit({
            'row': i,
            'col': 2,
            'text': str(read_num)
        })
        space = int(self._visit_space_input.text())
        time.sleep(space)

    def _is_reset_proxy(self):
        """
        是否重置代理
        :return:
        """
        self._lock.acquire()
        if not self._proxies:
            self._get_proxy()
        self._lock.release()

    def _visit_single(self, articles):
        """
        访问文章
        :param articles:
        :return:
        """
        visitor = RequestVisitor()
        while self._running and not self._proxies.empty():
            proxy = self._proxies.get()
            for i in range(len(articles)):
                if not self._running:
                    self.log_text_signal.emit('停止线程:{}...'.format(str(threading.currentThread().ident)))
                    return
                self._is_reset_proxy()
                is_visit = random.choice([True, False])
                if is_visit:
                    self._lock.acquire()
                    raw_read_num = int(self._articles_table.item(i, 2).text())  # 文章列表显示的访问量
                    self._lock.release()
                    read_num = visitor.visit(articles[i]['url'], proxy)

                    self.update_table_view(articles, i, read_num, raw_read_num)

    def _get_proxy_single(self):
        """
        获取1页代理
        :param page
        :return:
        """
        self.log_text_signal.emit('正在获取免费代理...')
        proxy_obj = QuickProxy(2)
        proxies = proxy_obj.get_all()
        proxies.reverse()
        for pro in proxies:
            self._proxies.put(pro)
            self.log_text_signal.emit('代理:{}'.format(pro))
        self.log_text_signal.emit('获取免费代理完成...')

    def _get_proxies(self):
        """
        多线程补充代理, 60秒补充一次
        :return:
        """
        while True:
            proxy_obj = QuickProxy(20)
            proxies = proxy_obj.get_all()
            for pro in proxies:
                self._proxies.put(pro)
                self.log_text_signal.emit('补充代理:{}' .format(pro))
            time.sleep(60)

    def _update_table_read_num(self, data):
        """
        :return:
        """
        self._articles_table.item(data['row'], data['col']).setText(data['text'])

    def _show_article_to_table(self, articles):
        """
        将文章列表展示到表格中
        :param articles:
        :return:
        """
        for art in articles:
            row = self._articles_table.rowCount()
            self._articles_table.insertRow(row)
            items = [art['title'], art['url'], art['read_num']]

            for j in range(len(items)):
                item = QTableWidgetItem(str(items[j]))
                self._articles_table.setItem(row, j, item)

    def _show_to_log(self, text):
        """
        显示文字并滚动到最后
        :param text:
        :return:
        """
        self._log_text_browser.append(text)
        self._log_text_browser.moveCursor(self._log_text_browser.textCursor().End)

    def stop(self):
        self._running = False
        self._is_start = False
        QMessageBox.information(self, MESSAGE_TITLE, '程序已停止！', QMessageBox.Yes)

    def destroy(self):
        """
        销毁应用
        :return:
        """
        is_ok = QMessageBox.question(self, MESSAGE_TITLE, '确认退出程序?', QMessageBox.Yes | QMessageBox.No)
        if is_ok == QMessageBox.Yes:
            os._exit(5)

    def select_visit_model(self):
        """
        选择访问模式
        :return:
        """
        pass

    def import_proxy(self):
        """
        导入代理
        :return:
        """
        file_select = QFileDialog.getOpenFileName(self, '导入代理', os.path.abspath(os.getcwd()), 'Text Files (*.txt)')
        if not file_select[0]:
            self.log_text_signal.emit('未选择文件!')
            return
        self.log_text_signal.emit('选择从文件: {}导入!'.format(file_select[0]))
        try:
            data = []
            with open(file_select[0], 'r', encoding='utf-8-sig') as f:
                for line in f:
                    proxy = {
                        'http': 'http://{}'.format(line.strip()),
                    }
                    data.append(proxy)
            random.shuffle(data)
            for pro in data:
                self._proxies.put(pro)
                self.log_text_signal.emit('导入一条代理:{}'.format(pro))

            self.log_text_signal.emit('成功导入{}个代理.'.format(str(self._proxies.qsize())))

        except Exception as e:
            print(e.args)
            self.log_text_signal.emit('导入失败: ' + str(e.args))
            QMessageBox.information(self, MESSAGE_TITLE, '导入代理失败，请检测文件内容格式和编码(utf8)！', QMessageBox.Yes)


def start_window():
    """
    启动窗体
    :return:
    """
    app = QApplication(sys.argv)
    w = Window()
    w.setWindowTitle('CSDN刷访问量')
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_window()