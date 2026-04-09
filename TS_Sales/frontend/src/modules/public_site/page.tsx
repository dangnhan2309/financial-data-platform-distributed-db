'use client';

export default function PublicSitePage() {
    return (
        <div>
            {/* Navigation Bar */}
            <nav className="fixed top-0 w-full bg-white shadow-md z-50 border-b-4 border-primary-700">
                <div className="max-w-6xl mx-auto px-6 py-2 flex items-center justify-between">
                    <div className="flex items-center">
                        <img
                            src="https://gcfood.com.vn/static/uploads/logo_GC_Food_ffaff2c3f8.svg"
                            alt="GC Food Logo"
                            className="h-20 object-contain py-2"
                        />
                    </div>
                    <div className="hidden md:flex gap-8 items-center">
                        <a href="#about" className="text-gray-700 hover:text-primary-700 font-medium">Giới thiệu</a>
                        <a href="#products" className="text-gray-700 hover:text-primary-700 font-medium">Sản phẩm</a>
                        <a href="#features" className="text-gray-700 hover:text-primary-700 font-medium">Đặc điểm</a>
                        <a href="#contact" className="text-gray-700 hover:text-primary-700 font-medium">Liên hệ</a>
                        <button className="bg-primary-700 text-white px-6 py-2 rounded-lg hover:bg-primary-800 font-semibold">
                            Đăng nhập
                        </button>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section
                className="pt-24 min-h-screen flex items-center relative overflow-hidden"
                style={{
                    backgroundImage: 'linear-gradient(to right, rgba(255,255,255,0.9), rgba(255,255,255,0.8), rgba(255,255,255,0.7)), url("https://gcfood.com.vn/static/uploads/banner_1_9e29d3f680.jpg")',
                    backgroundSize: 'cover',
                    backgroundPosition: 'center right',
                    backgroundAttachment: 'fixed'
                }}
            >
                {/* Decorative shapes */}
                <div className="absolute top-20 right-0 w-96 h-96 bg-primary-300/10 rounded-full blur-3xl"></div>
                <div className="absolute bottom-0 left-0 w-96 h-96 bg-accent-dark/5 rounded-full blur-3xl"></div>

                <div className="max-w-6xl mx-auto px-6 py-20 flex items-center gap-12 relative z-10">
                    <div className="flex-1">
                        <div className="inline-block bg-primary-100 text-primary-700 px-4 py-2 rounded-full mb-6 font-semibold text-sm">
                            ✨ Cam kết chất lượng quốc tế
                        </div>
                        <h1 className="text-6xl font-bold text-primary-800 mb-4 leading-tight">
                            Nông Sản Sạch<br />Xuất Khẩu Chất Lượng
                        </h1>
                        <p className="text-xl text-gray-700 mb-8 leading-relaxed max-w-lg">
                            GC Food là tập đoàn dẫn đầu thị trường Việt Nam về sản xuất và xuất khẩu Nha đam (VietFarm) và Thạch dừa (VinaCoco) với tiêu chuẩn quốc tế.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4">
                            <button className="bg-primary-700 text-white px-8 py-4 rounded-lg hover:bg-primary-800 text-lg font-semibold shadow-lg hover:shadow-xl transition-all">
                                📧 Yêu cầu Báo giá
                            </button>
                            <button className="border-3 border-primary-700 text-primary-700 px-8 py-4 rounded-lg hover:bg-primary-50 text-lg font-semibold transition-all">
                                🏢 Tìm hiểu thêm
                            </button>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-3 gap-6 mt-12">
                            <div>
                                <div className="text-3xl font-bold text-primary-700">50+</div>
                                <p className="text-gray-600 text-sm">Quốc gia xuất khẩu</p>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-primary-700">15K+</div>
                                <p className="text-gray-600 text-sm">Tấn/năm</p>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-primary-700">ISO</div>
                                <p className="text-gray-600 text-sm">BRC GlobalGAP</p>
                            </div>
                        </div>
                    </div>

                    <div className="flex-1 relative hidden lg:block">
                        <div className="absolute inset-0 bg-gradient-to-br from-primary-300 to-accent-DEFAULT rounded-3xl transform -rotate-6 opacity-30"></div>
                        <div className="relative bg-white rounded-3xl p-12 shadow-2xl border-4 border-accent-DEFAULT">
                            <div className="space-y-6 text-center">
                                <div className="text-7xl animate-pulse">🌾</div>
                                <h3 className="text-3xl font-bold text-primary-700">VietFarm</h3>
                                <p className="text-gray-600 text-lg">Nha đam - Từ thiên nhiên đến nhà bạn</p>
                                <div className="h-1 w-20 bg-primary-700 mx-auto rounded-full"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* About Section */}
            <section id="about" className="py-24 bg-white">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-5xl font-bold text-primary-700 mb-4">Về GC Food</h2>
                        <p className="text-xl text-gray-600 max-w-2xl mx-auto">Tập đoàn tiên phong trong ngành sản xuất và xuất khẩu nông sản công nghiệp</p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-12">
                        {/* VietFarm */}
                        <div className="rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-shadow border-4 border-primary-300 bg-gradient-to-br from-primary-50 to-white">
                            <div className="p-10">
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="text-5xl">🌿</div>
                                    <h3 className="text-3xl font-bold text-primary-700">VietFarm</h3>
                                </div>
                                <h4 className="text-2xl font-bold text-primary-800 mb-4">Nha Đam - Sức sống từ thiên nhiên</h4>
                                <p className="text-gray-700 mb-6 leading-relaxed">
                                    Nhà máy VietFarm chuyên sản xuất và xuất khẩu nha đam tươi, nha đam xay, nha đam dạng lỏng với tiêu chuẩn quốc tế. Sản phẩm được ứng dụng rộng rãi trong ngành F&B, trà sữa, nước giải khát và mỹ phẩm.
                                </p>
                                <div className="space-y-3">
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Chứng nhận ISO, BRC, GlobalGAP, FSSC 22000</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Xuất khẩu đến 50+ quốc gia</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Công suất: 5,000 tấn/năm</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Công nghệ sản xuất hiện đại</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* VinaCoco */}
                        <div className="rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-shadow border-4 border-secondary-300 bg-gradient-to-br from-secondary-50 to-white">
                            <div className="p-10">
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="text-5xl">🥥</div>
                                    <h3 className="text-3xl font-bold text-primary-700">VinaCoco</h3>
                                </div>
                                <h4 className="text-2xl font-bold text-primary-800 mb-4">Thạch Dừa - Kình đạo mát lạnh</h4>
                                <p className="text-gray-700 mb-6 leading-relaxed">
                                    Nhà máy VinaCoco sản xuất thạch dừa, sữa dừa cô đặc, bột dừa sấy với công nghệ sản xuất tiên tiến. Được tin dùng bởi các thương hiệu hàng đầu trong ngành công nghiệp thực phẩm toàn cầu.
                                </p>
                                <div className="space-y-3">
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Công nghệ Hydro-Colloid tiên tiến</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Sản phẩm làm mát tốt nhất kelasnya</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Công suất: 10,000 tấn/năm</span>
                                    </div>
                                    <div className="flex items-center gap-3 text-primary-700">
                                        <span className="text-2xl">✅</span>
                                        <span className="font-semibold">Xuất khẩu 60+ quốc gia</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Products Section */}
            <section id="products" className="py-24 bg-gradient-to-b from-accent-light to-white">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-5xl font-bold text-primary-700 mb-4">Sản Phẩm Chính</h2>
                        <p className="text-xl text-gray-600 max-w-2xl mx-auto">Bộ sưu tập đa dạng sản phẩm chất lượng cao từ VietFarm và VinaCoco</p>
                    </div>

                    <div className="grid md:grid-cols-4 gap-6">
                        {[
                            { name: 'Nha đam cắt hạt', desc: 'Tươi mới, sạch sẽ', image: 'https://kaizenco.vn/wp-content/uploads/2022/10/ad1a466e4e88e33ba0a0996e8adff4ef.jpg', color: 'from-primary-50' },
                            { name: 'Nha đam xay', desc: 'Tinh nguyên chất', image: 'https://hoaanhdao.vn/img/08/files/TIEN/6/7/1/cham-soc-toc-2.jpg', color: 'from-primary-100' },
                            { name: 'Nha đam lỏng', desc: 'Đã xử lý, sẵn dùng', image: 'https://gcfood.com.vn/static/uploads/small_tac_dung_cua_nha_dam_ap_dung_tinh_chat_nha_dam_tai_nha_cho_lan_da_khoe_manh_c6e345abfd.jpg', color: 'from-primary-200' },
                            { name: 'Thạch dừa', desc: 'Nguyên liệu cao cấp', image: 'https://gcfood.com.vn/static/uploads/san_pham_thach_dua_gc_food_15e757eff74d41eaa0f9e17a891777ee_master1_3347397e3e.jpg', color: 'from-secondary-100' },
                            { name: 'Sữa dừa cô đặc', desc: '40% Brix, chất lượng A', image: 'https://www.thtbstore.com/cdn/shop/files/6_899785d7-7801-4fbc-a570-b032aa003a30_600x.png?v=1715592810', color: 'from-secondary-200' },
                            { name: 'Bột dừa sấy', desc: 'Hàm lượng chất béo cao', image: 'https://dolambanhdanang.com/wp-content/uploads/2023/08/dua-vun-say-kho-100g-1691298217.jpeg', color: 'from-secondary-300' },
                            { name: 'Nước dừa tươi', desc: 'Vô trùng, tiệt trùng', image: 'https://vn.foodland.sk/sub/foodland.sk/shop/product/cgfood-napoj-z-mladeho-kokosu-325ml-797.jpg', color: 'from-accent-light' },
                            { name: 'Dừa sấy lạnh', desc: 'Giữ nguyên hương vị', image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2OxTJGonJ2IXSS7p-B0VEKQPB7ZFhPMAgUA&s', color: 'from-accent-DEFAULT' },
                        ].map((product, idx) => (
                            <div key={idx} className={`bg-gradient-to-br ${product.color} to-white rounded-xl shadow-lg hover:shadow-xl transition-all hover:-translate-y-2 p-8 border-2 border-primary-200 flex flex-col`}>
                                <img src={product.image} alt={product.name} className="w-full h-48 object-cover rounded-lg mb-4" />
                                <h4 className="text-lg font-bold text-primary-800 mb-2">{product.name}</h4>
                                <p className="text-sm text-gray-600 mb-4 flex-grow">{product.desc}</p>
                                <button className="w-full bg-primary-700 text-white py-2 rounded-lg hover:bg-primary-800 font-semibold text-sm">
                                    Chi tiết
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-24 bg-white">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-5xl font-bold text-primary-700 mb-4">Tại sao chọn GC Food?</h2>
                        <p className="text-xl text-gray-600">Cam kết chất lượng, uy tín và dịch vụ tốt nhất</p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        {[
                            { title: 'Chất lượng Quốc tế', desc: 'Tuân thủ các tiêu chuẩn ISO, BRC, GlobalGAP, FSSC 22000', icon: '🏆' },
                            { title: 'Xuất khẩu Rộng', desc: 'Sản phẩm bán cho 50+ quốc gia trong 5 châu lục', icon: '🌍' },
                            { title: 'Công nghệ Hiện đại', desc: 'Trang thiết bị sản xuất và kiểm chất tiên tiến', icon: '⚙️' },
                            { title: 'Phục vụ Chuyên nghiệp', desc: 'Đội ngũ sale ngoại thương, kỹ thuật, kế toán giàu kinh nghiệm', icon: '👥' },
                            { title: 'Giá cạnh tranh', desc: 'Tối ưu chi phí sản xuất, cung cấp giá hợp lý', icon: '💰' },
                            { title: 'Giao hàng nhanh', desc: 'Hạ tầng logistics mạnh, giao hàng toàn cầu', icon: '📦' },
                        ].map((feature, idx) => (
                            <div key={idx} className="bg-gradient-to-br from-accent-light to-white p-8 rounded-xl shadow-md hover:shadow-lg transition-all border-l-4 border-primary-700">
                                <div className="text-5xl mb-4">{feature.icon}</div>
                                <h3 className="text-xl font-bold text-primary-700 mb-2">{feature.title}</h3>
                                <p className="text-gray-600">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Contact CTA */}
            <section id="contact" className="py-24 bg-gradient-to-r from-primary-700 via-primary-600 to-primary-700 text-white relative overflow-hidden">
                <div className="absolute inset-0 opacity-10">
                    <div className="absolute top-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
                </div>

                <div className="max-w-4xl mx-auto px-6 relative z-10 text-center">
                    <h2 className="text-5xl font-bold mb-6 leading-tight">Sẵn sàng hợp tác cùng GC Food?</h2>
                    <p className="text-2xl mb-12 text-primary-50">
                        Liên hệ ngay để nhận báo giá và thông tin chi tiết về sản phẩm
                    </p>

                    <form className="max-w-3xl mx-auto bg-white rounded-2xl p-10 text-gray-900 shadow-2xl">
                        <div className="grid md:grid-cols-2 gap-6 mb-6">
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">Tên công ty</label>
                                <input
                                    type="text"
                                    placeholder="Nhập tên công ty của bạn"
                                    className="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary-700 focus:ring-2 focus:ring-primary-200"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
                                <input
                                    type="email"
                                    placeholder="email@company.com"
                                    className="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary-700 focus:ring-2 focus:ring-primary-200"
                                />
                            </div>
                        </div>

                        <div className="mb-6">
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Sản phẩm quan tâm</label>
                            <select className="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary-700 focus:ring-2 focus:ring-primary-200">
                                <option>--- Chọn sản phẩm ---</option>
                                <option>Nha đam (VietFarm)</option>
                                <option>Thạch dừa (VinaCoco)</option>
                                <option>Cả hai</option>
                            </select>
                        </div>

                        <div className="mb-6">
                            <label className="block text-sm font-semibold text-gray-700 mb-2">Thông tin thêm</label>
                            <textarea
                                placeholder="Vui lòng mô tả nhu cầu của bạn..."
                                rows={4}
                                className="w-full border-2 border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:border-primary-700 focus:ring-2 focus:ring-primary-200"
                            ></textarea>
                        </div>

                        <button
                            type="submit"
                            className="w-full bg-primary-700 text-white py-4 rounded-lg hover:bg-primary-800 font-bold text-lg shadow-lg hover:shadow-xl transition-all"
                        >
                            🚀 Gửi Yêu cầu ngay
                        </button>
                    </form>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-primary-900 text-white py-16">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="grid md:grid-cols-4 gap-12 mb-12">
                        <div>
                            <div className="flex items-center gap-2 mb-4">
                                <div className="text-2xl">🌾</div>
                                <h4 className="font-bold text-2xl">GC Food</h4>
                            </div>
                            <p className="text-primary-200 text-sm leading-relaxed">
                                Tập đoàn dẫn đầu thị trường. Sản phẩm chất lượng  quốc tế. Dịch vụ tuyệt vời.
                            </p>
                        </div>
                        <div>
                            <h4 className="font-bold text-lg mb-6">Sản phẩm</h4>
                            <ul className="space-y-3 text-primary-200">
                                <li><a href="#" className="hover:text-white transition">🌿 Nha đam (VietFarm)</a></li>
                                <li><a href="#" className="hover:text-white transition">🥥 Thạch dừa (VinaCoco)</a></li>
                                <li><a href="#" className="hover:text-white transition">📦 Các sản phẩm khác</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-bold text-lg mb-6">Công ty</h4>
                            <ul className="space-y-3 text-primary-200">
                                <li><a href="#" className="hover:text-white transition">Về GC Food</a></li>
                                <li><a href="#" className="hover:text-white transition">Tin tức</a></li>
                                <li><a href="#" className="hover:text-white transition">Tuyển dụng</a></li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-bold text-lg mb-6">Liên hệ</h4>
                            <div className="space-y-3 text-primary-200">
                                <p className="flex items-center gap-2"><span>📧</span> sales@gcfood.com</p>
                                <p className="flex items-center gap-2"><span>📞</span> +84 (0)28 xxxx xxxx</p>
                                <p className="flex items-center gap-2"><span>📍</span> TP.HCM, Việt Nam</p>
                            </div>
                        </div>
                    </div>

                    <div className="border-t border-primary-800 pt-8">
                        <div className="grid md:grid-cols-2 gap-8">
                            <p className="text-primary-200">
                                &copy; 2024 GC Food. Tất cả quyền được bảo vệ.
                            </p>
                            <div className="flex justify-end gap-6">
                                <a href="#" className="text-primary-200 hover:text-white transition">Điều khoản sử dụng</a>
                                <a href="#" className="text-primary-200 hover:text-white transition">Chính sách bảo mật</a>
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
}
