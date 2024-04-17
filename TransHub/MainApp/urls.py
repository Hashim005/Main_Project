
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('', views.showIndex, name='showindex'),
    path('SignUp/', views.SignUp,name='signup'),
    path('about/', views.about, name='about'),
    path('login/', views.Log, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.Home, name='Home'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('validateGlobalEmail/', views.validateGlobalEmail, name="validateGlobalEmail"),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('StaffSignUp/', views.Staff_signUp, name='Staff_signUp'),
    path('adminhome/', views.Admin_Home, name='Admin_Home'),
    path('adminusertable/', views.user_account, name='user_account'),

    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),  
    
    #path('activate/<uidb64>/<token>',views.ActivateAccount.as_view(),name='activate'),
    path('deactivation_email/',views.activatation_email,name='activatation_email'),
    path('activation_email/',views.deactivation_email,name='deactivation_email'),

    path('update_profile/',views.update_profile,name='update_profile'),
    path('profile/',views.profile,name='profile'),
    path('category/',views.category_mgt,name='category-page'),
    path('save_category/',views.save_category,name='save-category'),
    path('manage-category', views.manage_category, name='manage-category'),
    path('manage-category/<int:pk>/', views.manage_category, name='manage-category'),
    path('delete_category',views.delete_category,name='delete-category'),
    path('location',views.location_mgt,name='location-page'),
    path('manage_location',views.manage_location,name='manage-location'),
    path('save_location',views.save_location,name='save-location'),
    path('manage_location/<int:pk>',views.manage_location,name='manage-location-pk'),
    path('delete_location',views.delete_location,name='delete-location'),
    path('bus',views.bus_mgt,name='bus-page'),
    path('manage_bus',views.manage_bus,name='manage-bus'),
    path('save_bus',views.save_bus,name='save-bus'),
    path('manage_bus/<int:pk>',views.manage_bus,name='manage-bus-pk'),
    path('delete_bus',views.delete_bus,name='delete-bus'),
    path('schedule',views.schedule_mgt,name='schedule-page'),
    path('manage_schedule',views.manage_schedule,name='manage-schedule'),
    path('save_schedule',views.save_schedule,name='save-schedule'),
    path('manage_schedule/<int:pk>',views.manage_schedule,name='manage-schedule-pk'),
    path('delete_schedule',views.delete_schedule,name='delete-schedule'),
    path('bus-seat-map/', views.bus_seat_map, name='bus_seat_map'),
    path('book-seat/', views.book_seat, name='book_seat'),
    path('find_trip/',views.find_trip,name='find_trip'),
    path('schedule_view_page/<str:journey_date>/', views.schedule_view_page, name='schedule_view_page'),

    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('feedback_thankyou/', views.feedback_thankyou, name='feedback_thankyou'), 
    path("adminfeedback",views.adminfeedback,name='adminfeedback'),
    # path('seat_reservation/<str:code>', views.seat_reservation, name='seat_reservation'),

    # path('seat_reservation/<str:code>/<str:seats>/<int:total>/', views.seat_reservation, name='seat_reservation'),

    # path('passenger_details/', views.passenger_details, name='passenger_details'),
    path('seat_reservation/<str:schedule_code>/<int:schedule_id>/', views.seat_reservation, name='seat_reservation'),


    path('seatReservation/', views.seatReservation, name='seatReservation'),
    path('passengers/', views.passengers, name='passengers'),
    path('payments/', views.payments_view, name='payments'),
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('index1/', views.index1, name='index1'),
    path('warehoseindex/', views.warehouseindex, name='warehoseindex'),
    path('warehosueregister/', views.warehouse_signup_page, name='warehouseregister'),
    path('terms_and_condition/', views.terms_and_condition, name='terms_and_condition'),
    path('warehouselogin/', views.warehouse_login_page, name='warehouselogin'),
    path('warehouseprofile/', views.warehouse_profile_page, name='warehouse_profile_page'), 
    path('dropdown/', views.drop_down, name='dropdown'),
    path('admin_warehouse/', views.admin_warehouse, name='admin_warehouse'),
    path('warehouse_staff/', views.warehouse_staff, name='warehouse_staff'),
    path('warehouse_orders/', views.warehouse_orders, name="warehouse_orders"),
    path('warehouse_products/', views.warehouse_products, name='warehouse_products'),

    path('inventory_view/', views.inventory_view, name='inventory_view'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('edit_stock/<int:stock_id>/', views.edit_stock, name='edit_stock'),
    path('delete_stock/<int:stock_id>/', views.delete_stock, name='delete_stock'),
    path('add_stock_page/', views.add_stock_page, name='add_stock_page'),
    path('edit_stock_page/<int:stock_id>/',views.edit_stock_page, name='edit_stock_page'),
    path('get_stock_details/', views.get_stock_details, name='get_stock_details'),

    # path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    # path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    # path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    # path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    # path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),

    path('supplier_page/', views.supplier_page, name='supplier_page'),
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('request_accepting_page/', views.request_accepting_page, name='request_accepting_page'),
    path('accept_supplier/', views.accept_supplier, name='accept_supplier'),
    path('reject_supplier/', views.reject_supplier, name='reject_supplier'),

    path('sale_stock/', views.sale_stock, name='sale_stock'),
    

    path('supplier_selection/', views.supplier_selection, name='supplier_selection'),
    path('new_purchase/', views.new_purchase, name='new_purchase'),

    # warehose-main view
    path('warehouse_view/', views.warehouse_view, name='warehouse_view'),
    path('add/', views.add_warehouse, name='add_warehouse'),
    path('edit/<int:pk>/', views.edit_warehouse, name='edit_warehouse'),
    path('delete/<int:pk>/', views.delete_warehouse, name='delete_warehouse'),
    path('search-warehouse/', views.search_warehouse, name='search_warehouse'),

    # storage type
    path('storage_type/', views.storage_type, name='storage_type'),
    path('add_storage_type/', views.add_storage_type, name='add_storage_type'),
    path('edit_storage_type/<int:storage_type_id>/', views.edit_storage_type, name='edit_storage_type'),
    path('delete_storage_type/<int:storage_type_id>/', views.delete_storage_type, name='delete_storage_type'),
    path('error_view/', views.togle_view, name='error_view'),

    path('warehouse_template/', views.warehouse_template_page, name='warehouse_template'),
    path('warehouse_booking/', views.warehouse_booking_page, name='warehouse_booking'),
    path('storage_user_details/', views.storage_user_details, name='storage_user_details'),
    path('payment/', views.payment_page, name='payment_page'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
   
]
