import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="健康餐助手（手机版）", layout="centered")
st.title("🥗 健康餐助手 — 全周不重复菜单（手机友好）")

# ---------------- 用户输入 ----------------
col1, col2, col3 = st.columns(3)
with col1:
    height = st.number_input("身高 (cm)", 100, 250, 170)
with col2:
    weight = st.number_input("体重 (kg)", 30, 200, 65)
with col3:
    age = st.number_input("年龄", 10, 100, 25)

gender = st.selectbox("性别", ["男", "女"])
goal = st.selectbox("目标", ["减脂", "保持", "增肌"])

# ---------------- 计算每日目标 ----------------
bmr = 10*weight + 6.25*height - 5*age + (5 if gender=="男" else -161)
factor = 1.2 if goal=="减脂" else 1.4 if goal=="保持" else 1.6
sex_adj = 1.05 if gender=="男" else 0.95
calories_per_day = int(bmr * factor * sex_adj)
protein_g = int(weight * (1.8 if gender=="男" else 1.6))
fat_g = int(calories_per_day*0.25/9)
carb_g = int(calories_per_day*0.5/4)

st.markdown(f"**每日目标**：热量 {calories_per_day} kcal ｜ 蛋白质 {protein_g} g ｜ 碳水 ≈ {carb_g} g ｜ 脂肪 ≈ {fat_g} g")

# ---------------- 食物库 ----------------
food_db = {
    "鸡胸肉":{"cal":165,"p":31,"c":0,"f":3.6}, "牛肉":{"cal":250,"p":26,"c":0,"f":15},
    "三文鱼":{"cal":208,"p":20,"c":0,"f":13}, "鸡蛋":{"cal":155,"p":13,"c":1,"f":11},
    "燕麦片":{"cal":389,"p":17,"c":66,"f":7}, "糙米":{"cal":111,"p":2.6,"c":23,"f":0.9},
    "红薯":{"cal":86,"p":1.6,"c":20,"f":0.1}, "西兰花":{"cal":55,"p":3.7,"c":11,"f":0.6},
    "菠菜":{"cal":23,"p":2.9,"c":3.6,"f":0.4}, "坚果":{"cal":607,"p":20,"c":21,"f":54},
    "酸奶":{"cal":59,"p":10,"c":3.6,"f":0.4}, "香蕉":{"cal":89,"p":1.1,"c":23,"f":0.3},
    "豆腐":{"cal":76,"p":8,"c":1.9,"f":4.8}, "全麦面包":{"cal":247,"p":13,"c":41,"f":4.2},
    "藜麦":{"cal":120,"p":4,"c":21,"f":1.9}, "鸡腿肉":{"cal":215,"p":26,"c":0,"f":12},
    "鳕鱼":{"cal":82,"p":18,"c":0,"f":1}, "虾仁":{"cal":85,"p":20,"c":0,"f":1.2},
    "土豆":{"cal":77,"p":2,"c":17,"f":0.1}, "青椒":{"cal":20,"p":1,"c":4,"f":0.2},
    "番茄":{"cal":18,"p":0.9,"c":3.9,"f":0.2}, "蘑菇":{"cal":22,"p":3.1,"c":3.3,"f":0.3},
    "苹果":{"cal":52,"p":0.3,"c":14,"f":0.2}, "蓝莓":{"cal":57,"p":0.7,"c":14,"f":0.3},
    "橙子":{"cal":47,"p":0.9,"c":12,"f":0.1}, "草莓":{"cal":33,"p":0.7,"c":8,"f":0.3},
    "猕猴桃":{"cal":61,"p":1.1,"c":15,"f":0.5}, "低脂牛奶":{"cal":42,"p":3.4,"c":5,"f":1},
    "蛋白棒":{"cal":200,"p":20,"c":15,"f":5}, "花生酱":{"cal":588,"p":25,"c":20,"f":50},
    "牛油果":{"cal":160,"p":2,"c":9,"f":15}, "黄瓜":{"cal":16,"p":0.7,"c":3.6,"f":0.1},
    "胡萝卜":{"cal":41,"p":0.9,"c":10,"f":0.2}
}

# ---------------- 餐池 ----------------
breakfast_pool = [
    {"protein":"鸡蛋","carb":"全麦面包","fruit":"苹果"},
    {"protein":"燕麦片","carb":"燕麦片","fruit":"香蕉"},
    {"protein":"酸奶","carb":"燕麦片","fruit":"蓝莓"},
    {"protein":"蛋白棒","carb":"全麦面包","fruit":"橙子"},
    {"protein":"鸡蛋","carb":"全麦面包","fruit":"草莓"},
    {"protein":"低脂牛奶","carb":"燕麦片","fruit":"香蕉"},
    {"protein":"酸奶","carb":"全麦面包","fruit":"猕猴桃"}
]

lunch_pool = [
    {"protein":"鸡胸肉","carb":"糙米","veg":"西兰花"},
    {"protein":"三文鱼","carb":"糙米","veg":"菠菜"},
    {"protein":"牛肉","carb":"红薯","veg":"四季豆"},
    {"protein":"豆腐","carb":"糙米","veg":"蘑菇"},
    {"protein":"鸡胸肉","carb":"全麦面包","veg":"菠菜"},
    {"protein":"三文鱼","carb":"藜麦","veg":"西兰花"},
    {"protein":"牛肉","carb":"糙米","veg":"胡萝卜"}
]

dinner_pool = [
    {"protein":"鳕鱼","carb":"红薯","veg":"菠菜"},
    {"protein":"火鸡胸肉","carb":"糙米","veg":"芦笋"},
    {"protein":"豆腐","carb":"全麦面包","veg":"蘑菇"},
    {"protein":"鸡腿肉","carb":"土豆","veg":"西兰花"},
    {"protein":"三文鱼","carb":"藜麦","veg":"青椒"},
    {"protein":"牛肉","carb":"土豆","veg":"菠菜"},
    {"protein":"虾仁","carb":"全麦面包","veg":"番茄"}
]

snack_pool = [
    {"protein":"酸奶","fruit":"蓝莓"}, {"protein":"胡萝卜","veg":"黄瓜"}, {"protein":"苹果","fat":"坚果"},
    {"protein":"蛋白棒","protein2":"低脂牛奶"}, {"protein":"花生酱","carb":"全麦面包"},
    {"protein":"坚果","fruit":"香蕉"}, {"protein":"牛油果","protein2":"蛋白棒"}, {"protein":"酸奶","fruit":"猕猴桃"}
]

# ---------------- 辅助函数 ----------------
def grams_for_protein(food_key, target_p):
    info = food_db.get(food_key)
    if not info: return 50
    return max(50, int(target_p*100/info["p"]))

def allocate_meal(meal_template, protein_target, cal_target):
    items=[]
    prot_keys = [meal_template.get("protein"), meal_template.get("protein2")]
    for k in prot_keys:
        if k:
            g = grams_for_protein(k, protein_target/len([x for x in prot_keys if x]))
            info=food_db.get(k)
            cal=int(info["cal"]*g/100); p=int(info["p"]*g/100); c=int(info["c"]*g/100); f=int(info["f"]*g/100)
            items.append((k,g,cal,p,c,f))
    for role in ["carb","veg","fruit","fat"]:
        k = meal_template.get(role)
        if k:
            info=food_db.get(k)
            g=100; cal=int(info["cal"]*g/100); p=int(info["p"]*g/100); c=int(info["c"]*g/100); f=int(info["f"]*g/100)
            items.append((k,g,cal,p,c,f))
    # 热量微调
    total_cal=sum(it[2] for it in items)
    if total_cal>0:
        adjust_ratio = cal_target / total_cal
        new_items=[]
        for name,g,cal,p,c,f in items:
            g=int(g*adjust_ratio)
            info=food_db.get(name)
            new_items.append((name,g,int(info["cal"]*g/100),int(info["p"]*g/100),int(info["c"]*g/100),int(info["f"]*g/100)))
        items=new_items
    sum_cal=sum(it[2] for it in items)
    sum_p=sum(it[3] for it in items)
    sum_c=sum(it[4] for it in items)
    sum_f=sum(it[5] for it in items)
    return items,int(sum_cal),int(sum_p),int(sum_c),int(sum_f)

def generate_week_menu(breakfast_pool,lunch_pool,dinner_pool,snack_pool,protein_g,calories_per_day):
    week=[]
    random.shuffle(breakfast_pool)
    random.shuffle(lunch_pool)
    random.shuffle(dinner_pool)
    random.shuffle(snack_pool)
    for i in range(7):
        day={}
        day["早餐"]=allocate_meal(breakfast_pool[i%len(breakfast_pool)], protein_g*0.2, calories_per_day*0.25)
        day["午餐"]=allocate_meal(lunch_pool[i%len(lunch_pool)], protein_g*0.35, calories_per_day*0.35)
        day["晚餐"]=allocate_meal(dinner_pool[i%len(dinner_pool)], protein_g*0.3, calories_per_day*0.25)
        day["加餐"]=allocate_meal(snack_pool[i%len(snack_pool)], protein_g*0.15, calories_per_day*0.15)
        week.append(day)
    return week

def generate_week_summary(week):
    rows=[]
    for idx,day in enumerate(week,1):
        total_cal=sum(v[1] for v in day.values())
        total_p=sum(v[2] for v in day.values())
        total_c=sum(v[3] for v in day.values())
        total_f=sum(v[4] for v in day.values())
        rows.append([f"第{idx}天",total_cal,total_p,total_c,total_f])
    df=pd.DataFrame(rows,columns=["天数","总热量","总蛋白质","总碳水","总脂肪"])
    return df

def generate_shopping_list(week):
    shopping={}
    for day in week:
        for meal in day.values():
            for name,g,_,_,_,_ in meal:
                shopping[name]=shopping.get(name,0)+g
    return shopping

# ---------------- 生成按钮 ----------------
if st.button("生成一周菜单"):
    week = generate_week_menu(breakfast_pool,lunch_pool,dinner_pool,snack_pool,protein_g,calories_per_day)
    
    # 一周概要
    st.subheader("📊 一周概要")
    st.dataframe(generate_week_summary(week), use_container_width=True)
    
    # 每日详情
    st.subheader("📅 每日详情")
    for idx, day in enumerate(week,1):
        with st.expander(f"第 {idx} 天 — 总热量 {sum(v[1] for v in day.values())} kcal"):
            for meal_name, meal in day.items():
                items, cal, p, c, f = meal
                st.markdown(f"**{meal_name}** — 热量 {cal} kcal ｜ 蛋白质 {p} g ｜ 碳水 {c} g ｜ 脂肪 {f} g")
                st.dataframe(pd.DataFrame(items,columns=["食物","克数","热量","蛋白质","碳水","脂肪"]), use_container_width=True)
    
    # 一周购物清单
    st.subheader("🛒 一周购物清单")
    shopping = generate_shopping_list(week)
    for k,v in shopping.items():
        st.markdown(f"- {k}: {v} g")
