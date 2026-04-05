from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None

    if request.method == "POST":
        try:
            modal = float(request.form["modal"])
            jual = float(request.form["jual"])
            diskon = float(request.form["diskon"])
            ongkir = float(request.form["ongkir"])
            fee = float(request.form["fee"])

            # perhitungan
            harga_setelah_diskon = jual - (jual * diskon / 100)
            potongan_diskon = jual * diskon / 100
            potongan_fee = harga_setelah_diskon * fee / 100
            profit = harga_setelah_diskon - modal - ongkir - potongan_fee
            persen = (profit / modal) * 100

            # insight
            if jual < modal:
                insight = "Harga jual lebih rendah dari modal, pasti rugi."
            elif profit > 50000:
                insight = "Bisnis sangat menguntungkan."
            elif profit > 0:
                insight = "Masih untung, tapi bisa ditingkatkan."
            else:
                insight = "Rugi, pertimbangkan strategi ulang."

            hasil = {
                "harga_diskon": round(harga_setelah_diskon, 2),
                "profit": round(profit, 2),
                "persen": round(persen, 2),
                "diskon": round(potongan_diskon, 2),
                "fee": round(potongan_fee, 2),
                "insight": insight
            }

        except:
            hasil = {
                "harga_diskon": 0,
                "profit": 0,
                "persen": 0,
                "diskon": 0,
                "fee": 0,
                "insight": "Terjadi kesalahan input."
            }

    return render_template("index.html", hasil=hasil)


@app.route("/profil")
def profil():
    return render_template("profil.html")


if __name__ == "__main__":
    app.run(debug=True)