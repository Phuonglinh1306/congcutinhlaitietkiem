import streamlit as st
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    layout="centered"
)

st.title("TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Tính toán tiền lãi theo phương pháp lãi đơn và lãi kép.")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100000.0,
    step=100000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

phuong_phap = st.selectbox(
    "Phương pháp tính lãi",
    ["Lãi đơn", "Lãi kép"]
)

hinh_thuc_lanh = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)


# =========================
# TÍNH TOÁN
# =========================
if st.button("TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    # Lãi suất tháng
    lai_suat_thang = lai_suat / 100 / 12

    du_lieu = []
    tong_lai = 0

    # ==================================================
    # LÃI ĐƠN
    # ==================================================
    if phuong_phap == "Lãi đơn":

        # Lãnh lãi theo tháng
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            lai_moi_thang = so_tien * lai_suat_thang

            for thang in range(1, ky_han + 1):

                tong_lai += lai_moi_thang

                du_lieu.append({
                    "Kỳ": thang,
                    "Thời gian": f"Tháng {thang}",
                    "Tiền lãi định kỳ": lai_moi_thang,
                    "Tổng tiền lãi": tong_lai
                })

        # Lãnh lãi theo quý
        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            ky = 1
            thang_da_tinh = 0

            while thang_da_tinh < ky_han:

                so_thang = min(3, ky_han - thang_da_tinh)

                lai_ky = so_tien * lai_suat_thang * so_thang

                tong_lai += lai_ky

                du_lieu.append({
                    "Kỳ": ky,
                    "Thời gian": f"Quý {ky}",
                    "Tiền lãi định kỳ": lai_ky,
                    "Tổng tiền lãi": tong_lai
                })

                thang_da_tinh += so_thang
                ky += 1

        # Lãnh lãi cuối kỳ
        else:

            tong_lai = so_tien * lai_suat_thang * ky_han

            du_lieu.append({
                "Kỳ": 1,
                "Thời gian": f"Sau {ky_han} tháng",
                "Tiền lãi định kỳ": tong_lai,
                "Tổng tiền lãi": tong_lai
            })

    # ==================================================
    # LÃI KÉP
    # ==================================================
    else:

        von_hien_tai = so_tien

        # Lãnh lãi theo tháng
        if hinh_thuc_lanh == "Lãnh lãi theo tháng":

            for thang in range(1, ky_han + 1):

                lai_ky = von_hien_tai * lai_suat_thang

                von_hien_tai += lai_ky
                tong_lai += lai_ky

                du_lieu.append({
                    "Kỳ": thang,
                    "Thời gian": f"Tháng {thang}",
                    "Tiền lãi định kỳ": lai_ky,
                    "Tổng tiền lãi": tong_lai
                })

        # Lãnh lãi theo quý
        elif hinh_thuc_lanh == "Lãnh lãi theo quý":

            ky = 1
            thang_da_tinh = 0

            while thang_da_tinh < ky_han:

                so_thang = min(3, ky_han - thang_da_tinh)

                lai_ky = von_hien_tai * (
                    (1 + lai_suat_thang) ** so_thang - 1
                )

                von_hien_tai += lai_ky
                tong_lai += lai_ky

                du_lieu.append({
                    "Kỳ": ky,
                    "Thời gian": f"Quý {ky}",
                    "Tiền lãi định kỳ": lai_ky,
                    "Tổng tiền lãi": tong_lai
                })

                thang_da_tinh += so_thang
                ky += 1

        # Lãnh lãi cuối kỳ
        else:

            tong_tien_tiet_kiem = so_tien * (
                (1 + lai_suat_thang) ** ky_han
            )

            tong_lai = tong_tien_tiet_kiem - so_tien

            du_lieu.append({
                "Kỳ": 1,
                "Thời gian": f"Sau {ky_han} tháng",
                "Tiền lãi định kỳ": tong_lai,
                "Tổng tiền lãi": tong_lai
            })


    # =========================
    # TỔNG TIỀN
    # =========================
    tong_tien = so_tien + tong_lai


    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.success("Tính toán thành công.")

    st.subheader("Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Số tiền gửi",
            format_money(so_tien)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_money(tong_lai)
        )

    with col3:
        st.metric(
            "Tổng gốc và lãi",
            format_money(tong_tien)
        )


    # =========================
    # THÔNG TIN KHOẢN GỬI
    # =========================
    st.subheader("Thông tin khoản gửi")

    st.write(f"Phương pháp tính: {phuong_phap}")
    st.write(f"Hình thức lãnh lãi: {hinh_thuc_lanh}")
    st.write(f"Kỳ hạn: {ky_han} tháng")
    st.write(f"Lãi suất: {lai_suat:.2f}%/năm")


    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.subheader("Chi tiết tiền lãi định kỳ")

    df = pd.DataFrame(du_lieu)

    df["Tiền lãi định kỳ"] = df["Tiền lãi định kỳ"].apply(
        format_money
    )

    df["Tổng tiền lãi"] = df["Tổng tiền lãi"].apply(
        format_money
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # =========================
    # TỔNG KẾT
    # =========================
    st.subheader("Tổng kết")

    st.write(
        f"Số tiền gửi ban đầu: {format_money(so_tien)}"
    )

    st.write(
        f"Tổng tiền lãi: {format_money(tong_lai)}"
    )

    st.write(
        f"Tổng số tiền gốc và lãi: {format_money(tong_tien)}"
    )
