
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from accounts.forms import UserCreateForm, ProfileForm


# Create your views here.


class RegisterView(CreateView):
    form_class = UserCreateForm
    # success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

    def get_success_url(self):
        login(self.request, self.object)
        return reverse_lazy('Project_list')

@login_required
def edite_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=request.user)
        form.save()
        return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
        return render(request,'profile.html',{'form':form})