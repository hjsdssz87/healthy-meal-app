import streamlit as st
import random

st.set_page_config(page_title="健康餐助手", layout="centered")
st.title("🥗 健康餐助手 - 性别+目标自适应菜单")

# 用户输入
height = st.number_input("身高 (cm)", 100, 250, 170)
weight = st.number_input("体重 (kg)", 30, 200, 65)
gender = st.selectbox("你的性别", ["男", "女"])
goal = st.selectbox("你的目标", ["减脂", "保持", "增肌"])

age = 25

# 基础代谢率 (BMR)
bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender=="男" else -161)

# 目标系数
factor = 1.2 if goal=="减脂" else 1.4 if goal=="保持" else 1.6
calories_per_day = int(bmr * factor * (1.05 if gender=="男" else 0.95))

# 蛋白质、碳水、脂肪目标
protein_g = int(weight * (1.8 if gender=="男" else 1.6))
fat_g = int(calories_per_day*0.25/9)
carb_g = int(calories_per_day*0.5/4)

st.markdown(f"**每日营养目标**: 热量 {calories_per_day} kcal | 蛋白质 {protein_g} g | 碳水 {carb_g} g | 脂肪 {fat_g} g")

# 食物库（每100g含量示例）
food_db = {
    "鸡胸肉": {"cal":165,"protein":31,"carb":0,"fat":3.6},
    "牛肉": {"cal":250,"protein":26,"carb":0,"fat":15},
    "三文鱼": {"cal":208,"protein":20,"carb":0,"fat":13},
    "火鸡胸肉": {"cal":135,"protein":30,"carb":0,"fat":1},
    "鸡蛋": {"cal":155,"protein":13,"carb":1,"fat":11},
    "燕麦片": {"cal":389,"protein":17,"carb":66,"fat":7},
    "糙米": {"cal":111,"protein":2.6,"carb":23,"fat":0.9},
    "红薯": {"cal":86,"protein":1.6,"carb":20,"fat":0.1},
    "西兰花": {"cal":55,"protein":3.7,"carb":11,"fat":0.6},
    "菠菜": {"cal":23,"protein":2.9,"carb":3.6,"fat":0.4},
    "芦笋": {"cal":20,"protein":2.2,"carb":3.9,"fat":0.1},
    "四季豆": {"cal":31,"protein":1.8,"carb":7,"fat":0.1},
    "玉米": {"cal":86,"protein":3.2,"carb":19,"fat":1.2},
    "全麦面包": {"cal":247,"protein":13,"carb":41,"fat":4.2},
    "坚果": {"cal":607,"protein":20,"carb":21,"fat":54},
    "酸奶": {"cal":59,"protein":10,"carb":3.6,"fat":0.4},
    "香蕉": {"cal":89,"protein":1.1,"carb":23,"fat":0.3},
    "豆腐": {"cal":76,"protein":8,"carb":1.9,"fat":4.8}
}

# 性别菜单选择
if gender=="男":
    breakfast_options = [["燕麦片","牛奶","鸡蛋"],["全麦面包","鸡蛋","香蕉"],["酸奶","燕麦片","香蕉"]]
    lunch_options = [["鸡胸肉","西兰花","糙米"],["牛肉","红薯","西兰花"],["三文鱼","菠菜","糙米"]]
    dinner_options = [["鸡胸肉","芦笋","糙米"],["三文鱼","玉米","红薯"],["火鸡胸肉","四季豆","全麦面包"]]
    snack_options = [["坚果","香蕉"],["酸奶","水果"],["蛋白棒"]]
else:
    breakfast_options = [["燕麦片","酸奶","香蕉"],["全麦面包","鸡蛋","水果"],["酸奶","燕麦片","水果"]]
    lunch_options = [["鸡胸肉","菠菜","糙米"],["豆腐","红薯","西兰花"],["三文鱼","菠菜","糙米"]]
    dinner_options = [["鸡胸肉","芦笋","红薯"],["三文鱼","玉米","红薯"],["豆腐","四季豆","全麦面包"]]
    snack_options = [["坚果","水果"],["酸奶","水果"],["蛋白棒"]]

if st.button("生成一周饮食计划"):
    week_meals=[]
    for day in range(1,8):
        breakfast = random.choice(breakfast_options)
        lunch = random.choice(lunch_options)
        snack = random.choice(snack_options)
        dinner = random.choice(dinner_options)
        week_meals.append([breakfast,lunch,snack,dinner])

    st.subheader("📅 一周饮食计划")
    for day, meals in enumerate(week_meals,1):
        with st.expander(f"第 {day} 天"):
            for meal_name, meal in zip(["早餐","午餐","加餐","晚餐"], meals):
                total_cal=total_protein=total_carb=total_fat=0
                meal_text=[]
                for food in meal:
                    g = 100  # 默认克数
                    if food in food_db:
                        f = food_db[food]
                        cal = f["cal"]*g/100
                        protein = f["protein"]*g/100
                        carb = f["carb"]*g/100
                        fat = f["fat"]*g/100
                        total_cal += cal
                        total_protein += protein
                        total_carb += carb
                        total_fat += fat
                        meal_text.append(f"{food} {g}g")
                st.markdown(f"**{meal_name}**: {', '.join(meal_text)} | 热量: {int(total_cal)} kcal, 蛋白质: {int(total_protein)} g, 碳水: {int(total_carb)} g, 脂肪: {int(total_fat)} g")

    # 购物清单
    shopping_list={}
    for meals in week_meals:
        for meal in meals:
            for food in meal:
                shopping_list[food]=shopping_list.get(food,0)+100

    st.subheader("🛒 一周购物清单")
    for food, qty in shopping_list.items():
        st.markdown(f"- {food}: {qty*7//len(week_meals)} g")
