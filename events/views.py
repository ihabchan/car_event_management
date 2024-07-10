from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import CustomUser, Post, Merch, Cart, Wishlist, Event, Purchase, EventParticipant
from .forms import LoginForm, PostForm, CustomUserCreationForm, MerchForm, EventForm, MerchPurchaseForm, TicketPurchaseForm, EventParticipantForm

User = get_user_model()

def home(request):
    return render(request, 'home.html')

def gallery(request):
    posts = Post.objects.all()
    return render(request, 'gallery.html', {'posts': posts})

def event(request):
    events = Event.objects.all()
    return render(request, 'event.html', {'events': events})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                elif user.is_staff:
                    return redirect('staff_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    staff_users = User.objects.filter(is_staff=True)
    return render(request, 'admin_dashboard.html', {'staff_users': staff_users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_staff(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, 'Staff account created successfully.')
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_staff.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def view_purchases(request):
    purchases = Purchase.objects.all()
    return render(request, 'view_purchases.html', {'purchases': purchases})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('gallery')
    return render(request, 'delete_post.html', {'post': post})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def create_merch(request):
    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('merch')
    else:
        form = MerchForm()
    return render(request, 'create_merch.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def update_merch(request, merch_id):
    merch = get_object_or_404(Merch, pk=merch_id)
    if request.method == 'POST':
        form = MerchForm(request.POST, request.FILES, instance=merch)
        if form.is_valid():
            form.save()
            return redirect('merch')
    else:
        form = MerchForm(instance=merch)
    return render(request, 'update_merch.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_merch(request, item_id):
    merch = get_object_or_404(Merch, id=item_id)
    if request.method == 'POST':
        merch.delete()
        messages.success(request, 'Merchandise deleted successfully.')
        return redirect('merch')
    return render(request, 'confirm_delete.html', {'merch': merch})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully.')
            return redirect('event')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event')
    else:
        form = EventForm(instance=event)
    return render(request, 'update_event.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event')
    return render(request, 'delete_event.html', {'event': event})

def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to add items to your cart.")
        return redirect('login')
    product = get_object_or_404(Merch, pk=item_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1, 'price': product.price}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('merch')

def add_to_wishlist(request, item_id):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to add items to your wishlist.")
        return redirect('login')
    product = get_object_or_404(Merch, pk=item_id)
    Wishlist.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'price': product.price}
    )
    messages.success(request, f'Added {product.name} to your wishlist.')
    return redirect('merch')

def cart(request):
    if not request.user.is_authenticated:
        return render(request, 'access_denied.html')
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)

def wishlist(request):
    if not request.user.is_authenticated:
        return render(request, 'access_denied.html')
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

def merch(request):
    products = Merch.objects.all()
    context = {
        'products': products,
        'is_logged_in': request.user.is_authenticated,
    }
    return render(request, 'merch.html', context)

@login_required
def purchase_merch(request, item_id):
    product = get_object_or_404(Merch, pk=item_id)
    if request.method == 'POST':
        form = MerchPurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.merch = product
            purchase.total_price = product.price * purchase.quantity
            purchase.save()
            messages.success(request, 'Purchase completed successfully.')
            return redirect('user_dashboard')
    else:
        form = MerchPurchaseForm(initial={'merch': product})
    return render(request, 'purchase_merch.html', {'form': form, 'product': product})

@login_required
def purchase_event_ticket(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.event = event
            purchase.total_price = 10
            purchase.save()
            messages.success(request, 'Ticket purchased successfully.')
            return redirect('user_dashboard')
    else:
        form = TicketPurchaseForm()
    return render(request, 'purchase_event_ticket.html', {'form': form, 'event': event})

@login_required
def participate_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user = request.user
            participant.event = event
            participant.payment = 200 
            participant.save()
            messages.success(request, 'You have successfully registered to participate in the event.')
            return redirect('user_dashboard')
    else:
        form = EventParticipantForm()
    return render(request, 'participate_event.html', {'form': form, 'event': event})

@login_required
def user_dashboard(request):
    events = Event.objects.all()
    merch_items = Merch.objects.all() 
    context = {
        'events': events,
        'merch_items': merch_items,
    }
    return render(request, 'user_dashboard.html', context)

@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.info(request, "Your cart is empty.")
        return redirect('cart')

    total_price = sum(item.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = MerchPurchaseForm (request.POST, request.FILES)
        if form.is_valid():
            cart_items.delete()  
            messages.success(request, 'Purchase completed successfully.')
            return redirect('user_dashboard')
    else:
        form = MerchPurchaseForm ()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    }
    return render(request, 'checkout.html', context)

@login_required
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.is_staff:
        return redirect('staff_dashboard')
    else:
        return redirect('user_dashboard')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def track_staff(request):
    staff_list = CustomUser.objects.filter(is_staff=True)
    return render(request, 'track_staff.html', {'staff_list': staff_list})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_staff(request, staff_id):
    staff = get_object_or_404(CustomUser, id=staff_id, is_staff=True)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Staff member deleted successfully.')
        return redirect('track_staff')
    return render(request, 'confirm_delete.html', {'staff': staff})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=item_id)
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
        return redirect('cart')
    return render(request, 'remove_from_cart.html', {'cart_item': cart_item})
