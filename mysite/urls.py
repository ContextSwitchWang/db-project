# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls import include, url
from django.contrib import admin

from polls.views import index
from django.http import HttpResponse

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('supplychain.urls')),
    url(r'^.well-known/acme-challenge/oS1VK6tCBRbFVkloMhKKNchPS9d4InuBHGMacMKrzno$', 
        lambda r: HttpResponse('oS1VK6tCBRbFVkloMhKKNchPS9d4InuBHGMacMKrzno.ylKeLZEHEpTWJYco-iY94ZYtUL4Cz3C4AhX_LfxjzZk')),
    url(r'^.well-known/acme-challenge/nZY7tD5KBulKhRXkJcARk26_JCrSSquMHo_ElgOOGo4', 
        lambda r: HttpResponse('nZY7tD5KBulKhRXkJcARk26_JCrSSquMHo_ElgOOGo4.ylKeLZEHEpTWJYco-iY94ZYtUL4Cz3C4AhX_LfxjzZk')),
]
