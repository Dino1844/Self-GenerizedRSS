# kit.py

import tkinter
import tkinter.messagebox
import customtkinter
import feedparser
import db # type: ignore
import crawler # type: ignore

# 默认设置
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    # 主交互框架
    def __init__(self):
        # 全继承
        super().__init__()

        # 画布
        self.title("CustomTkinter complex_example.py")
        self.geometry("1100x580")

        # 整体布局
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6), weight=1)  
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1) 
        
        # 侧边栏
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0,column=0,rowspan=13,sticky="nsew")
        
        # 侧边栏按键
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="RSS", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10)) 
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="新的信息",command=self.show_mainpage)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)  
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="我的订阅",command=self.show_subscription)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10) 
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="更新文章",command=self.refresh)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10) 
 
        # 侧边栏黑白mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # 添加的部分
        self.entry = customtkinter.CTkEntry(self,placeholder_text="输入RSS源")
        self.main_button_1 = customtkinter.CTkButton(master=self, text="添加订阅",
                                                     fg_color="transparent",
                                                     border_width=2, 
                                                     text_color=("gray10"),
                                                     command = self.add_subscription)

        #连接数据库
        self.conn = db.connect("rss.db")
        self.cursor = db.new_cursor(self.conn)
        db.new_table_website(self.cursor,"rss_feeds","URL","WEB_NAME")
    # 刷新按钮
    def refresh(self):
        #测试
        # print("button1 click")
        # 隐藏
        
        self.cursor.execute("SELECT * FROM rss_feeds")
        feeds = self.cursor.fetchall()

        for feed in feeds:
            
            feed_url = feed[1]
            index = db.get_index(self.cursor,feed_url)
            db.new_table_article(self.cursor,name = "web"+str(index),
                                 column1 = "title",
                                 column2="link",
                                 column3="publish_date")
            feed_data = feedparser.parse(feed_url)
            for entry in feed_data.entries:
                self.cursor.execute("SELECT * FROM {} WHERE title = ?".format("web"+str(index)), (entry.title,))
                existing_feed = self.cursor.fetchone()
                if existing_feed:
                    continue
                self.cursor.execute("""
                                    INSERT INTO {} (title, link, publish_date) 
                                    VALUES (?, ?, ?)
                                    """.format("web"+str(index)),(entry.title, entry.link, entry.published)
                )
            self.conn.commit()
            
        print("success")
    # 改变颜色,抄官方文档
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    # 文章分析界面,提供爬虫api
    def show_mainpage(self):
        self.main_page_frame = customtkinter.CTkScrollableFrame(self)
        self.main_page_frame.grid(row=0, column=3, sticky="nsew")
        self.table_frame.grid_remove()
        self.entry.grid_remove()
        self.main_button_1.grid_remove()
        self.table_frame.grid(row=1, column=1, rowspan=10, columnspan=10, padx=20, pady=20, sticky="nsew")    
        titles = db.get_title_fromall(self.cursor)   
        for i,title in enumerate(titles):
            label = customtkinter.CTkLabel(self.main_page_frame, text=f"{title[0]}")
            label.grid(row=i+1,column=1, padx=10, pady=10, sticky="nsew")
            # !!! 可能=有bug
            num = 0
            #找接下来的标签,找到所在表的位置
            for j in range(i+1,i+1000):
                if title[i][0][:3] == "web":
                    num = int(title[i][0][4:])
            url = db.get_url(self.cursor,num = num,title = title[0])
            button = customtkinter.CTkButton(self.main_page_frame, text="@", command=lambda: self.pachong_api(url))
            button.grid(row=i+1, column=2, padx=10, pady=10, sticky="nsew")
    # 点击按钮即爬虫
    def pachong_api(self,url):
        article =  crawler.article(url = url)
        #!!! 这里先返回文章?返回给谁?
        return 
    # 在订阅模块显示现在的订阅
    def show_subscription(self):
        # 测试
        # print("button_2 click")
        # 显示输入组块
        self.table_frame = customtkinter.CTkScrollableFrame(self)
        self.table_frame.grid(row=1, column=1, rowspan=10, columnspan=10, padx=20, pady=20, sticky="nsew")
        self.entry.grid(row=12, column=1, rowspan=1, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.main_button_1.grid(row=12, column=5, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # 从数据库获得URL并且添加到table_frame里面
        self.cursor.execute("SELECT * FROM rss_feeds")
        feeds = self.cursor.fetchall()
        self.labels =[]
        for i,feed in enumerate(feeds):
            label = customtkinter.CTkLabel(self.table_frame, text=f"{feed[:3]}")
            label.grid(row=i+1,column=1, padx=10, pady=10, sticky="nsew")
            self.labels.append(label)
    # 添加订阅
    def add_subscription(self):
        # 获取用户输入的 RSS 订阅源 URL
        url = self.entry.get()
       # 检查 URL 是否已存在数据库中
        self.cursor.execute("SELECT * FROM rss_feeds WHERE url = ?", (url,))
        existing_feed = self.cursor.fetchone()
        if existing_feed:
            tkinter.messagebox.showinfo("提示", "该订阅源已存在")
            return
        # 解析标题
        feed_data = feedparser.parse(url)
        title = feed_data.feed.title

        # 将订阅源添加到数据库
        self.cursor.execute("INSERT INTO rss_feeds (url, web_name) VALUES (?, ?)", (url, title))
        self.conn.commit()

        # 清空输入框
        self.entry.delete(0, tkinter.END)
        tkinter.messagebox.showinfo("提示", "订阅源添加成功")
        self.show_subscription()

if __name__ == "__main__":
    app = App()
    app.mainloop()