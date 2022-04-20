from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
)
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.utils import timezone

from django.conf import settings
from django.core.mail import send_mail

from .forms import CreateUserForm, UserUpdateForm, UserPasswordChangeForm, AddressCreateForm, CheckOutForm
from .models import Address, City, District, Ward

from items.models import Order, OrderItem



User = get_user_model()


class UserCreateView(CreateView):
    form_class = CreateUserForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return redirect("login")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('items:home')
        return super(UserCreateView, self).get(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "user"
    template_name = "accounts/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address_qs = Address.objects.filter(user=self.request.user)
        context.update({
            'address_list': address_qs
        })
        return context

    def get_object(self, *args, **kwargs):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = "accounts/user_info_update.html"

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_success_url(self):
        messages.info(self.request, "Updated")
        return reverse("accounts:profile", kwargs={'pk': self.object.pk})


class PwdChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "registration/password_change.html"

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_success_url(self) -> str:
        messages.info(self.request, "Password Changed!")
        return reverse("accounts:profile", kwargs={'pk': self.request.user.pk})


class CreateAddressView(LoginRequiredMixin, CreateView):
    form_class = AddressCreateForm
    template_name = "addresses/address_create_form.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    form_class = AddressCreateForm
    template_name = "addresses/address_update.html"
    context_object_name = "address"
    success_url = reverse_lazy("accounts:profile")

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


def remove_address(request, pk):
    address_qs = Address.objects.filter(user=request.user, pk=pk)
    if address_qs.exists():
        address = address_qs[0]
        address.delete()
    else:
        pass
    return redirect("accounts:profile")


def load_district(request):
    city_id = request.GET.get('city')
    districts = District.objects.filter(city_id=city_id).order_by('name')
    return render(request, 'addresses/districts_dropdown_list_options.html', {'districts': districts})


def load_ward(request):
    district_id = request.GET.get('district')
    wards = Ward.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'addresses/ward_dropdown_list_options.html', {'wards': wards})


class CheckoutView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            'form': form,
        }

        order_qs = Order.objects.filter(user=self.request.user, order_state=False)
        if order_qs.exists():
            order = order_qs[0]
            items = OrderItem.objects.filter(order=order_qs[0])
            context.update({
                'order': order,
            })
            # Lấy danh sách item của order sau đó thêm vào context
            if items.exists():
                context.update({
                    'items': items,
                })
                # Lấy danh sách địa chỉ giao hàng của user sau đó thêm vào context
                addresses = Address.objects.filter(user=self.request.user)
                if addresses.exists():
                    context.update({'addresses': addresses})
                return render(self.request, 'accounts/checkout.html', context)

            else:  # Nếu không có sản phẩm nào của order
                messages.error(self.request, "Không có sản phẩm trong giỏ hàng!")
                return redirect("items:cart")
        # Nếu không có order
        else:
            messages.error(self.request, "Không có sản phẩm trong giỏ hàng!")
            return redirect("items:cart")

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        # print(self.request.POST)
        if form.is_valid() and 'address' in self.request.POST:
            # print("form",form.cleaned_data)
            address_id = self.request.POST['address']
            address = get_object_or_404(Address, user=self.request.user, pk=address_id)
            order_qs = Order.objects.filter(user=self.request.user, order_state=False)
            if order_qs.exists():
                order = order_qs[0]
                order.shipping_address = address
                order.order_state = True
                order.order_date = timezone.now()
                order.payment_method = self.request.POST['payment_option']
                order.save()

                # Gửi mail thông báo tới user
                subject = 'UNIQUE Shop đã tiếp nhận đơn hàng'
                email_msg = f'Xin chào {self.request.user.first_name} {self.request.user.last_name}, UNIQUE Shop đã tiếp nhận đơn hàng của bạn. Cảm ơn bạn đã đặt hàng tại cửa hàng của chúng tôi.'
                email_from = settings.EMAIL_HOST_USER
                email_to = [self.request.user.email, ]
                send_mail(subject, email_msg, email_from, email_to)

                # Gửi mail cho tài khoản admin
                admin_subject = f"Tiếp nhận đơn hàng mới từ {self.request.user.username}"
                admin_email_msg = f"Tiếp nhận đơn hàng mới từ {self.request.user.username}. Mã đơn hàng {order.pk}. Hình thức thanh toán: {form.cleaned_data['payment_option']}"
                admin = User.objects.get(username="admin")
                admin_email = [admin.email, ]
                send_mail(admin_subject, admin_email_msg, email_from, admin_email)
                return redirect('/')

        else:
            messages.error(self.request, "Vui lòng chọn địa chỉ giao hàng")
            return redirect('accounts:checkout')
