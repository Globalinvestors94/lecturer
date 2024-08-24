import functools
from django.shortcuts import redirect
from django.contrib import messages
from .models import Scratch_Pin,Profile
from django.http import HttpResponse,HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.urls import reverse


def PinCode(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
    	if request.method == 'POST':
    		pin = request.POST.get('pin')
    		reg = request.POST.get('reg_number')

    		print(pin)
    		print(reg)

    		# if pin:
    		try:
	    		scratch_n = Scratch_Pin.objects.get(number=pin)

    			if scratch_n == pin:
    				scratch_n.is_used = True
    				scratch_n.save()
    				return view_func(request, *args, **kwargs)

    			elif scratch_n.student_reg == 0:
    				scratch_n.student_reg = reg
    				scratch_n.usage_count += 1

    				scratch_n.save()
    				return view_func(request, *args, **kwargs)

    			elif scratch_n.usage_count >=1:
    				return view_func(request, *args, **kwargs)

    			elif scratch_n.usage_count >3:
    				return HttpResponse("Your scratch card has reached the maximum usuage.")

    			elif scratch_n.student_reg != reg:
    				scratch_n.student_reg = reg
    				scratch_n.save()
    				return view_func(request, *args, **kwargs)


    			elif scratch_n.student_reg is not None:
    				messages.success(request, "A student has purchased this scratch card")
    				return redirect("lecture:pin")



    			elif scratch_n.student_reg == reg:
    				messages.success(request, "A student has purchased this scratch card")
    				return redirect("lecture:pin")

    			else:
    				messages.success(request, "Please input the pin on your scratch card")
    				return redirect("lecture:pin")



    		except Scratch_Pin.DoesNotExist:
    			messages.success(request, "Pin incorrect")
    			return redirect("lecture:pin")

    	else:
    		messages.success(request, "Welcome")
    		return redirect("lecture:pin")
    return wrapper



def Prevent_Manual_Access(view_func):
	def _wrapped_view(request, *args, **kwargs):
		slug = kwargs.get('slug')
		pp = Profile.objects.all().values_list('slug')
		for pp in pp:
			if slug not in pp:
				return HttpResponseRedirect(reverse('/'))
			return view_func(request, *args, **kwargs)
	return _wrapped_view