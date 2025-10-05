# app.py — 智能营养餐助手 B版（蛋白质优先分配）
import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="智能营养餐助手", layout="centered")
st.title("🥗 智能营养餐助手")
st.caption("按 性别/年龄/身高/体重/目标 计算热量并优先满足蛋白质摄入，然后分配碳水/脂肪。")

# -------------------------
# 用户输入
# -------------------------
col1, col2, col3 = st.columns(3)
with col1:
    height = st.number_input("身高 (cm)", min_value=100, max_value=250, value=170)
with col2:
    weight = st.number_input("体重 (kg)", min_value=30, max_value=200, value=65)
with col3:
    age = st.number_input("年龄", min_value=10, max_value=100, value=25)

gender = st.selectbox("性别", ["男", "女"])
goal = st.selectbox("目标", ["减脂", "保持", "增肌"])

# -------------------------
# 计算每日目标（BMR + factor）
# -------------------------
if gender == "男":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

factor = 1.2 if goal == "减脂" else 1.4 if goal == "保持" else 1.6
sex_adj = 1.05 if gender == "男" else 0.95
calories_per_day = int(bmr * factor * sex_adj)

# 每日蛋白质目标（g）
protein_g = int(weight * (1.8 if gender == "男" else 1.6))
# 其他目标（近似）
fat_g = int(calories_per_day * 0.25 / 9)
carb_g = int(calories_per_day * 0.5 / 4)

st.markdown(f"**每日目标**：热量 {calories_per_day} kcal ｜ 蛋白质 {protein_g} g ｜ 碳水 ≈ {carb_g} g ｜ 脂肪 ≈ {fat_g} g")

# -------------------------
# 食物库（每100g营养值，中西混合）
# 注：p=蛋白质(g), c=碳水(g), f=脂肪(g), cal=kcal
# -------------------------
food_db = {
    "鸡胸肉":{"cal":165,"p":31,"c":0,"f":3.6},
    "鸡腿肉":{"cal":209,"p":26,"c":0,"f":11},
    "牛肉":{"cal":250,"p":26,"c":0,"f":15},
    "猪里脊":{"cal":242,"p":27,"c":0,"f":14},
    "三文鱼":{"cal":208,"p":20,"c":0,"f":13},
    "鳕鱼":{"cal":82,"p":18,"c":0,"f":0.7},
    "虾仁":{"cal":99,"p":24,"c":0.2,"f":0.3},
    "金枪鱼罐头":{"cal":132,"p":28,"c":0,"f":1},
    "豆腐":{"cal":76,"p":8,"c":1.9,"f":4.8},
    "鸡蛋":{"cal":155,"p":13,"c":1,"f":11},
    "燕麦片":{"cal":389,"p":17,"c":66,"f":7},
    "糙米":{"cal":111,"p":2.6,"c":23,"f":0.9},
    "白米饭":{"cal":130,"p":2.4,"c":28,"f":0.3},
    "红薯":{"cal":86,"p":1.6,"c":20,"f":0.1},
    "全麦面包":{"cal":247,"p":13,"c":41,"f":4.2},
    "藜麦":{"cal":120,"p":4.1,"c":21,"f":1.9},
    "意大利面":{"cal":131,"p":5,"c":25,"f":1.1},
    "土豆":{"cal":77,"p":2,"c":17,"f":0.1},
    "西兰花":{"cal":55,"p":3.7,"c":11,"f":0.6},
    "菠菜":{"cal":23,"p":2.9,"c":3.6,"f":0.4},
    "芦笋":{"cal":20,"p":2.2,"c":3.9,"f":0.1},
    "四季豆":{"cal":31,"p":1.8,"c":7,"f":0.1},
    "胡萝卜":{"cal":41,"p":0.9,"c":10,"f":0.2},
    "番茄":{"cal":18,"p":0.9,"c":3.9,"f":0.2},
    "黄瓜":{"cal":16,"p":0.7,"c":3.6,"f":0.1},
    "蘑菇":{"cal":22,"p":3.1,"c":3.3,"f":0.3},
    "青椒":{"cal":20,"p":0.9,"c":4.6,"f":0.2},
    "香蕉":{"cal":89,"p":1.1,"c":23,"f":0.3},
    "苹果":{"cal":52,"p":0.3,"c":14,"f":0.2},
    "蓝莓":{"cal":57,"p":0.7,"c":14,"f":0.3},
    "草莓":{"cal":33,"p":0.7,"c":8,"f":0.3},
    "橙子":{"cal":47,"p":0.9,"c":12,"f":0.1},
    "猕猴桃":{"cal":61,"p":1.1,"c":15,"f":0.5},
    "葡萄":{"cal":69,"p":0.7,"c":18,"f":0.2},
    "坚果":{"cal":607,"p":20,"c":21,"f":54},
    "牛油果":{"cal":160,"p":2,"c":9,"f":15},
    "橄榄油":{"cal":884,"p":0,"c":0,"f":100},
    "酸奶":{"cal":59,"p":10,"c":3.6,"f":0.4},
    "低脂牛奶":{"cal":42,"p":3.4,"c":5,"f":1},
    "蛋白棒":{"cal":250,"p":20,"c":23,"f":7},
    "花生酱":{"cal":588,"p":25,"c":20,"f":50},
    "芝麻":{"cal":573,"p":18,"c":23,"f":50}
}

# -------------------------
# 餐别池（明确标注蛋白/碳水/蔬菜/脂肪角色）
# 每个条目为 dict：{"protein":..., "carb":..., "veg":..., "fat":... (可选), "fruit":... (可选)}
# -------------------------
breakfast_pool = [
    {"protein":"鸡蛋","carb":"全麦面包","fruit":"苹果"},
    {"protein":"燕麦片","carb":"燕麦片","fruit":"香蕉"},  # 燕麦既碳水又可作蛋白来源（简化）
    {"protein":"酸奶","carb":"燕麦片","fruit":"蓝莓"},
    {"protein":"蛋白棒","carb":"全麦面包","fruit":"橙子"},
    {"protein":"鸡蛋","carb":"全麦面包","fruit":"草莓"},
    {"protein":"低脂牛奶","carb":"燕麦片","fruit":"香蕉"},
    {"protein":"酸奶","carb":"全麦面包","fruit":"猕猴桃"}
]

lunch_pool = [
    {"protein":"鸡胸肉","carb":"糙米","veg":"西兰花","fat":"牛油果"},
    {"protein":"三文鱼","carb":"藜麦","veg":"菠菜","fat":"橄榄油"},
    {"protein":"牛肉","carb":"土豆","veg":"四季豆"},
    {"protein":"虾仁","carb":"意大利面","veg":"番茄"},
    {"protein":"金枪鱼罐头","carb":"白米饭","veg":"黄瓜"},
    {"protein":"猪里脊","carb":"红薯","veg":"胡萝卜"},
    {"protein":"豆腐","carb":"糙米","veg":"蘑菇"}
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

snack_pool_fatloss = [
    {"protein":"酸奶","fruit":"蓝莓"},
    {"protein":"胡萝卜","veg":"黄瓜"},
    {"protein":"苹果","fat":"坚果"},
    {"protein":"草莓","protein2":"酸奶"},
    {"protein":"猕猴桃","fat":"坚果"},
    {"protein":"香蕉","protein2":"低脂牛奶"},
    {"protein":"酸奶","fruit":"葡萄"}
]
snack_pool_maintain = [
    {"protein":"酸奶","fruit":"香蕉"},
    {"protein":"坚果","fruit":"苹果"},
    {"protein":"蛋白棒","protein2":"低脂牛奶"},
    {"protein":"酸奶","fruit":"蓝莓"},
    {"protein":"花生酱","carb":"全麦面包"},
    {"protein":"牛油果","carb":"全麦面包"},
    {"protein":"酸奶","fruit":"草莓"}
]
snack_pool_gain = [
    {"protein":"蛋白棒","fat":"牛油果"},
    {"protein":"花生酱","carb":"全麦面包"},
    {"protein":"坚果","protein2":"酸奶"},
    {"protein":"蛋白棒","protein2":"低脂牛奶"},
    {"protein":"花生酱","carb":"全麦面包"},
    {"protein":"坚果","fruit":"香蕉"},
    {"protein":"牛油果","protein2":"蛋白棒"}
]

snack_pool = snack_pool_fatloss if goal=="减脂" else snack_pool_gain if goal=="增肌" else snack_pool_maintain

# -------------------------
# 蛋白质优先分配比例（按你要求）
# -------------------------
protein_ratio_per_meal = {"早餐":0.20, "午餐":0.35, "晚餐":0.30, "加餐":0.15}
meal_ratios = {"早餐":0.25, "午餐":0.35, "晚餐":0.25, "加餐":0.15}
gender_factor = 1.1 if gender=="男" else 0.9

# 推荐最小/最大克数保护
MIN_GRAMS = 20
MAX_GRAMS = 800

# -------------------------
# 工具函数：根据目标蛋白克数算蛋白食物克数
# -------------------------
def grams_for_protein_food(food_key, protein_target_g):
    """ 返回满足 protein_target_g 所需克数（基于 food_db 中的 p per 100g） """
    info = food_db.get(food_key)
    if not info or info.get("p",0) <= 0:
        return MIN_GRAMS
    p100 = info["p"]
    grams = int(max(MIN_GRAMS, protein_target_g * 100.0 / p100))
    grams = min(grams, MAX_GRAMS)
    return grams

def grams_for_calorie_target(food_key, cal_target):
    """ 返回满足 cal_target 所需克数（基于 food_db 中的 cal per 100g） """
    info = food_db.get(food_key)
    cal100 = info["cal"] if info else 100
    if cal100 <= 0:
        return MIN_GRAMS
    grams = int(max(MIN_GRAMS, cal_target * 100.0 / cal100))
    grams = min(grams, MAX_GRAMS)
    return grams

# -------------------------
# 分配一餐：优先满足蛋白质目标，然后按剩余热量分配其他项
# -------------------------
def allocate_meal(meal_template, meal_cal_target, protein_target_total_g):
    """
    meal_template: dict 包含 roles: protein, carb, veg, fat, fruit, protein2...
    meal_cal_target: 该餐目标热量（kcal）
    protein_target_total_g: 该餐蛋白质目标（g）
    返回： items list of tuples (name, grams, cal, p, c, f) 和汇总
    """
    items = []
    # 1) 先处理主蛋白
    prot_key = meal_template.get("protein")
    prot2_key = meal_template.get("protein2")  # 有时加餐会有两个蛋白来源
    used_cal = 0.0
    used_p = 0.0
    # 主蛋白
    if prot_key:
        g_prot = grams_for_protein_food(prot_key, protein_target_total_g)
        info = food_db.get(prot_key)
        cal = info["cal"] * g_prot / 100.0 if info else 0
        p = info["p"] * g_prot / 100.0 if info else 0
        c = info["c"] * g_prot / 100.0 if info else 0
        f = info["f"] * g_prot / 100.0 if info else 0
        items.append((prot_key, g_prot, int(cal), int(p), int(c), int(f)))
        used_cal += cal; used_p += p
    # 如果存在第二蛋白（如酸奶+坚果），按剩余蛋白目标分配一部分
    if prot2_key:
        # 剩余蛋白目标
        remaining_prot_target = max(0.0, protein_target_total_g - used_p)
        g_prot2 = grams_for_protein_food(prot2_key, remaining_prot_target)
        info = food_db.get(prot2_key)
        cal = info["cal"] * g_prot2 / 100.0 if info else 0
        p = info["p"] * g_prot2 / 100.0 if info else 0
        c = info["c"] * g_prot2 / 100.0 if info else 0
        f = info["f"] * g_prot2 / 100.0 if info else 0
        items.append((prot2_key, g_prot2, int(cal), int(p), int(c), int(f)))
        used_cal += cal; used_p += p

    # 2) 剩余热量用于其他角色
    remaining_cal = meal_cal_target - used_cal
    # 如果蛋白已经占满或超过（蛋白非常高的情况下），我们允许蛋白占主导，但限制不会超出餐热量的 90%
    if remaining_cal < meal_cal_target * 0.1:
        # 缩小蛋白份量到占比 0.6 * meal_cal_target（避免完全超标）
        cap_cal_from_protein = meal_cal_target * 0.6
        if used_cal > cap_cal_from_protein:
            scale = cap_cal_from_protein / used_cal
            # 按比例缩小已添加的蛋白食材克数
            new_items = []
            used_cal = 0.0; used_p = 0.0
            for (name, grams, cal, p, c, f) in items:
                new_grams = max(MIN_GRAMS, int(grams * scale))
                info = food_db.get(name)
                if info:
                    cal = info["cal"] * new_grams / 100.0
                    p = info["p"] * new_grams / 100.0
                    c = info["c"] * new_grams / 100.0
                    f = info["f"] * new_grams / 100.0
                else:
                    cal=p=c=f=0
                new_items.append((name, new_grams, int(cal), int(p), int(c), int(f)))
                used_cal += cal; used_p += p
            items = new_items
        remaining_cal = meal_cal_target - used_cal

    # 3) 对 carb / veg / fat / fruit 分配（使用简单权重）
    # 优先分配碳水（如果 meal_template 有 carb）
    role_weights = []
    if "carb" in meal_template: role_weights.append(("carb", 0.65))
    if "veg" in meal_template: role_weights.append(("veg", 0.2))
    # fat 和 fruit/others
    if "fat" in meal_template: role_weights.append(("fat", 0.15))
    if "fruit" in meal_template and "carb" not in meal_template:
        # 若没有明确碳水，把 fruit 视作碳水
        role_weights.append(("fruit", 0.65))
    # 归一化权重
    if role_weights:
        s = sum(w for _, w in role_weights)
        role_weights = [(r, w / s) for r, w in role_weights]
    # 分配
    for role, weight in role_weights:
        key = meal_template.get(role)
        if not key:
            continue
        cal_alloc = max(0.0, remaining_cal * weight)
        grams = grams_for_calorie_target(key, cal_alloc)
        info = food_db.get(key)
        if info:
            cal = info["cal"] * grams / 100.0
            p = info["p"] * grams / 100.0
            c = info["c"] * grams / 100.0
            f = info["f"] * grams / 100.0
        else:
            cal = grams * 0.8; p=c=f=0
        items.append((key, grams, int(cal), int(p), int(c), int(f)))
        used_cal += cal; used_p += p
        remaining_cal = meal_cal_target - used_cal

    # 4) 如果还有未分配热量（比如没有fat role），可在 veg 或 carb 上补足
    if remaining_cal > 30:
        # 找到第一个可扩展的角色进行补足（优先 carb -> veg -> fat）
        for role in ("carb","veg","fat","fruit"):
            key = meal_template.get(role)
            if key:
                grams_extra = grams_for_calorie_target(key, remaining_cal)
                info = food_db.get(key)
                if info:
                    cal = info["cal"] * grams_extra / 100.0
                    p = info["p"] * grams_extra / 100.0
                    c = info["c"] * grams_extra / 100.0
                    f = info["f"] * grams_extra / 100.0
                else:
                    cal = grams_extra * 0.8; p=c=f=0
                items.append((key, grams_extra, int(cal), int(p), int(c), int(f)))
                used_cal += cal; used_p += p
                remaining_cal = meal_cal_target - used_cal
                break

    # 汇总并返回
    sum_cal = sum(it[2] for it in items)
    sum_p = sum(it[3] for it in items)
    sum_c = sum(it[4] for it in items)
    sum_f = sum(it[5] for it in items)
    return items, int(sum_cal), int(sum_p), int(sum_c), int(sum_f)

# -------------------------
# 生成一天计划（按模板选择）和一周计划
# -------------------------
def random_choice_template(pool):
    return random.choice(pool)

def generate_day(plan_index=None):
    # 计算各餐蛋白质目标（g）按比例
    day = {}
    for meal_name in ["早餐","午餐","晚餐","加餐"]:
        meal_cal_target = calories_per_day * meal_ratios[meal_name]
        protein_target = protein_g * protein_ratio_per_meal[meal_name]
        # 选择模板
        if meal_name == "早餐":
            template = random_choice_template(breakfast_pool)
        elif meal_name == "午餐":
            template = random_choice_template(lunch_pool)
        elif meal_name == "晚餐":
            template = random_choice_template(dinner_pool)
        else:
            template = random_choice_template(snack_pool)
        items, cal, p, c, f = allocate_meal(template, meal_cal_target, protein_target)
        day[meal_name] = {"items": items, "cal": cal, "p": p, "c": c, "f": f, "template": template}
    return day

# -------------------------
# 主界面：生成一周并显示概要 + 可展开详情
# -------------------------
if st.button("生成一周菜单（蛋白优先）"):
    week = [generate_day(i) for i in range(7)]

    # 一周概要表
    rows = []
    for i, day in enumerate(week, 1):
        total_cal = sum(m["cal"] for m in day.values())
        total_p = sum(m["p"] for m in day.values())
        total_c = sum(m["c"] for m in day.values())
        total_f = sum(m["f"] for m in day.values())
        # 摘要：每餐第一个食材
        summary = []
        for mn in ["早餐","午餐","晚餐","加餐"]:
            it = day[mn]["items"]
            if it:
                summary.append(it[0][0])
            else:
                summary.append("-")
        rows.append({"第几天": f"第 {i} 天", "总热量(kcal)": int(total_cal), "蛋白质(g)": int(total_p), "碳水(g)": int(total_c), "脂肪(g)": int(total_f), "主要菜品": " / ".join(summary)})

    df = pd.DataFrame(rows)
    st.subheader("📊 一周概要")
    st.dataframe(df, use_container_width=True)

    # 每日详情（可展开）
    st.subheader("📅 每日详情（展开查看）")
    for i, day in enumerate(week, 1):
        with st.expander(f"第 {i} 天 — 总热量 {sum(m['cal'] for m in day.values())} kcal"):
            for mn in ["早餐","午餐","加餐","晚餐"]:
                meal = day[mn]
                st.markdown(f"**{mn}** — 热量 {meal['cal']} kcal ｜ 蛋白质 {meal['p']} g ｜ 碳水 {meal['c']} g ｜ 脂肪 {meal['f']} g")
                if meal["items"]:
                    df_meal = pd.DataFrame(meal["items"], columns=["食物","克数","热量(kcal)","蛋白质(g)","碳水(g)","脂肪(g)"])
                    st.dataframe(df_meal, use_container_width=True)
                else:
                    st.write("无食物数据。")

    # 周购物清单
    shopping = {}
    for day in week:
        for meal in day.values():
            for name, grams, *_ in meal["items"]:
                shopping[name] = shopping.get(name, 0) + grams

    st.subheader("🛒 一周购物清单（估算）")
    for k, v in shopping.items():
        st.markdown(f"- {k}: {v} g（约 {int(v/100)} 份100g）")
