import streamlit as st
import random

st.set_page_config(page_title="智能营养餐助手", layout="centered")
st.title("🥗 智能营养餐助手 - 扩充食物库 + 年龄自适应")

# 用户输入
height = st.number_input("身高 (cm)", 100, 250, 170)
weight = st.number_input("体重 (kg)", 30, 200, 65)
gender = st.selectbox("你的性别", ["男", "女"])
age = st.number_input("年龄", 10, 80, 25)
goal = st.selectbox("你的目标", ["减脂", "保持", "增肌"])

# 基础代谢率 (BMR) 考虑年龄
bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender=="男" else -161)

# 目标系数
factor = 1.2 if goal=="减脂" else 1.4 if goal=="保持" else 1.6
calories_per_day = int(bmr * factor * (1.05 if gender=="男" else 0.95))

# 蛋白质、碳水、脂肪目标
protein_g = int(weight * (1.8 if gender=="男" else 1.6))
fat_g = int(calories_per_day*0.25/9)
carb_g = int(calories_per_day*0.5/4)

st.markdown(f"**每日营养目标**: 热量 {calories_per_day} kcal | 蛋白质 {protein_g} g | 碳水 {carb_g} g | 脂肪 {fat_g} g")

# 扩充食物库（更多种类）
food_db = {
    # 蛋白质来源
    "鸡胸肉": {"cal":165,"protein":31,"carb":0,"fat":3.6},
    "牛肉": {"cal":250,"protein":26,"carb":0,"fat":15},
    "三文鱼": {"cal":208,"protein":20,"carb":0,"fat":13},
    "火鸡胸肉": {"cal":135,"protein":30,"carb":0,"fat":1},
    "鸡蛋": {"cal":155,"protein":13,"carb":1,"fat":11},
    "豆腐": {"cal":76,"protein":8,"carb":1.9,"fat":4.8},
    "虾": {"cal":99,"protein":24,"carb":0,"fat":0.3},
    "金枪鱼": {"cal":132,"protein":28,"carb":0,"fat":1},
    "鳕鱼": {"cal":82,"protein":18,"carb":0,"fat":0.7},
    "羊肉": {"cal":294,"protein":25,"carb":0,"fat":21},

    # 碳水来源
    "燕麦片": {"cal":389,"protein":17,"carb":66,"fat":7},
    "糙米": {"cal":111,"protein":2.6,"carb":23,"fat":0.9},
    "红薯": {"cal":86,"protein":1.6,"carb":20,"fat":0.1},
    "全麦面包": {"cal":247,"protein":13,"carb":41,"fat":4.2},
    "藜麦": {"cal":120,"protein":4.1,"carb":21,"fat":1.9},
    "意面": {"cal":131,"protein":5,"carb":25,"fat":1.1},
    "土豆": {"cal":77,"protein":2,"carb":17,"fat":0.1},

    # 蔬菜
    "西兰花": {"cal":55,"protein":3.7,"carb":11,"fat":0.6},
    "菠菜": {"cal":23,"protein":2.9,"carb":3.6,"fat":0.4},
    "芦笋": {"cal":20,"protein":2.2,"carb":3.9,"fat":0.1},
    "四季豆": {"cal":31,"protein":1.8,"carb":7,"fat":0.1},
    "胡萝卜": {"cal":41,"protein":0.9,"carb":10,"fat":0.2},
    "番茄": {"cal":18,"protein":0.9,"carb":3.9,"fat":0.2},
    "青椒": {"cal":20,"protein":0.9,"carb":4.6,"fat":0.2},

    # 水果
    "香蕉": {"cal":89,"protein":1.1,"carb":23,"fat":0.3},
    "苹果": {"cal":52,"protein":0.3,"carb":14,"fat":0.2},
    "蓝莓": {"cal":57,"protein":0.7,"carb":14,"fat":0.3},
    "草莓": {"cal":33,"protein":0.7,"carb":8,"fat":0.3},
    "橙子": {"cal":47,"protein":0.9,"carb":12,"fat":0.1},
    "猕猴桃": {"cal":61,"protein":1.1,"carb":15,"fat":0.5},

    # 脂肪及乳制品
    "坚果": {"cal":607,"protein":20,"carb":21,"fat":54},
    "牛油果": {"cal":160,"protein":2,"carb":9,"fat":15},
    "橄榄油": {"cal":884,"protein":0,"carb":0,"fat":100},
    "酸奶": {"cal":59,"protein":10,"carb":3.6,"fat":0.4},
    "奶酪": {"cal":402,"protein":25,"carb":1.3,"fat":33},
    "黄油": {"cal":717,"protein":0.9,"carb":0.1,"fat":81}
}

meal_targets = {"早餐": (0.25, 0.25, 0.25), "午餐": (0.35, 0.4, 0.35), "晚餐": (0.25, 0.25, 0.3), "加餐": (0.15, 0.1, 0.1)}

def generate_meal_plan():
    day_plan = {}
    for meal, (c_ratio, p_ratio, f_ratio) in meal_targets.items():
        selected_foods = random.sample(list(food_db.keys()), 3)
        meal_text = []
        total_cal = total_protein = total_carb = total_fat = 0
        for food in selected_foods:
            grams = 100
            f = food_db[food]
            cal = f["cal"]*grams/100
            protein = f["protein"]*grams/100
            carb = f["carb"]*grams/100
            fat = f["fat"]*grams/100
            total_cal += cal
            total_protein += protein
            total_carb += carb
            total_fat += fat
            meal_text.append(f"{food} {grams}g")
        day_plan[meal] = {"items": meal_text, "cal": int(total_cal), "protein": int(total_protein), "carb": int(total_carb), "fat": int(total_fat)}
    return day_plan

if st.button("生成一周饮食计划"):
    week_plan = [generate_meal_plan() for _ in range(7)]
    st.subheader("📅 一周饮食计划")
    for i, day in enumerate(week_plan, 1):
        with st.expander(f"第 {i} 天"):
            for meal, info in day.items():
                st.markdown(f"**{meal}**: {', '.join(info['items'])} | 热量: {info['cal']} kcal, 蛋白质: {info['protein']} g, 碳水: {info['carb']} g, 脂肪: {info['fat']} g")
    shopping_list = {}
    for day in week_plan:
        for meal in day.values():
            for item in meal['items']:
                food, grams = item.split()
                grams = int(grams[:-1])
                shopping_list[food] = shopping_list.get(food, 0) + grams
    st.subheader("🛒 一周购物清单")
    for food, qty in shopping_list.items():
        st.markdown(f"- {food}: {qty} g")
