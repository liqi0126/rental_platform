# rental platform

## dependency

```shell
pip install django-allauth
pip install django-phone-field
pip install djangorestframework
pip install django-rest-auth
pip install django-filter

pip install pyyaml
pip install uritemplate
```



## Data structure

### manager

* username (unique)
* password (注意加密)



### user

* username (unique)
* password (注意加密)
* created_at (创建时间)
* description
* address
* contact
* E-mail
* rent_applications(_id) (发出的租借申请)
* rented equipments(_id) (现在租借的设备)
* is_renter
  * renter_applications(_id) # 发出的成为【设备持有者】申请
  * release_applications(_id) # 发出的上线申请
  * received_rent_applications # 收到的租借申请
  * owned_equipments(_id) # 拥有的设备



### equipment

* name
* description
* address
* contact (联系方式)
* owner(_id)
* release_applications (上线申请历史)
* rent_applications (租借历史)
* current status
  * unrelased (设备提供者尚未申请上线或下线) 
  * unapproved (设备提供者申请上线，管理员审核中)
  * available (可租借)
  * rented (已经被租借)
    * current tenant(_id)
    * lease term begin (租借时间)
    * lease term end
  * returned but unchecked (用户已经返还，设备提供者尚未确认)
* comments （用户使用评价)



### renter_application

* applicant(_id)
* descriptions
* status
  * unapproved (已申请，管理员审核中)
  * accepted
  * rejected
* comments （管理员说明)



### release_application

* equipment(_id)
* owner(_id)
* descriptions
* status
  * unapproved (已申请，管理员审核中)
  * accepted
  * rejected
* comments (管理员说明)



### rent_application

* equipment(_id)

* renter(_id) (设备提供者)

* hirer(_id) (租借者)
* descriptions
  * usage (用途)
  * lease term (租借日期)
* status
  * unapproved (已申请，设备提供者审批中)
  * accepted
  * rejected
* comments (设备提供者说明)



***NOTE:*** update data concurrently, e.g., after we rent a equipment, we need to:

* add equipment id to user.rented_equipments
* change rent_application.status to accepted
* change equipment.status to rented
* etc...



## Front Route

### /resigter

（徐）

* 管理员可以 **创建新的管理员账户**
* 用户可以 **创建账户**

**NOTE:** 注册时要求所有用户必须和清华的学号或者工号绑定认证



### /login

（徐）

* 管理员可以 **登录账号**
* 用户可以 **登录账号**



### /statistic （for manager)

（徐）

管理员可以 

  * **查看设备、用户的统计信息**
  * **查询所有的请求记录**





### /user?page=:page

（李）

 * 管理员可以 **查询用户信息、设置用户类型、删除任意用户**



### /user/:user_id

（李）

 * 管理员可以 **设置用户类型、删除用户**
 * 设备提供者可以 
    * **查看、添加、删除、申请上架、下架自己的设备**
    * **查看自己的审批历史**
 * 用户可以 
    * **查看设备租借申请历史**
    * **查看已经借用到的设备及租借信息**
    * **对即将到期的设备给出一定的提示**
    * **申请成为设备提供者并查看申请状态**

### 

### /renter_application?page=:page 

（马）

* 管理员可以 **查看、审批、删除** 所有的【成为设备提供者】申请



### /renter_application/:renter_application_id

（马）

	* 管理员可以 **审批、删除** 【成为设备提供者】申请



### /release_application?page=:page/admin

（马）

* 管理员可以 **查看、审批、删除** 所有的【设备上架】申请
* 设备提供者可以 **提交、查看、删除(撤回)** 所有的【设备上架】申请



### /release_application/:release_applicaion_id

（马）

* 管理员可以 **审批、删除** 【设备上架】申请
* 设备提供者可以 **提交、编辑、删除(撤回)** 【设备上架】申请



### /rent_application?page=:page

（马）

	* 管理员可以 **查看、审批、删除** 所有的【租赁】申请
	* 设备提供者可以 **查看、审批** 关于自己设备的【租赁】申请
	* 用户可以 **查看、修改** 关于自己申请的【租赁】申请



### /rent_application/:rent_application_id

（马）

* 管理者可以 **查看、审批、删除** 【租赁】申请
* 设备提供者可以 **查看、审批** 【租赁】申请
* 用户可以
  *  **查看、修改、删除(即撤回)** 【租赁】申请
  * 设备提供结束后 **对设备进行评价**



### /equipments?page=:page

（丁）

* 管理员可以 **查询、修改、删除** 设备，可以看到所有 【等待审批】的设备
* 设备提供者可以 **查看、修改、添加、删除、申请上架、下架** 设备，可以看到自己【等待审批】的设备
* 用户可以 **查看、申请设备提供、返还** 设备，不可以看到【等待审批】的设备
* 展示出 设备名称、设备提供者、现在的状态 等内容
* 支持查询搜索



### /equipment/:equipment_id

（丁）

	* 管理员可以 **查询、修改、删除** 设备信息
	* 设备提供者可以 **查看、修改、删除、下架、确认归还** 设备
	* 用户可以 **查看、申请设备提供、返还** 设备
	* 展示出 设备名称、设备提供者、出借方地址、租期结束时间、联系方式、现在的状态 等内容





（optional)

### /chatroom

* 用户可以在线聊天





## API summary

POST：创建

GET：获取

PUT：更新（全部更新）

PATCH：部分更新

DELETE：删除



### user related

* POST /api/v1/login  # log in
* POST /api/v1/logout # log out
* GET/PUT/PATCH/DELETE /api/v1/users/:user-id
* POST /api/v1/users # 创建新用户
* GET /api/v1/users # 获取所有用户



### equipments related

* POST /api/v1/equipment # create a new equipment
* GET /api/v1/equipment # get all equipments
* GET /api/v1/equipment/:equipment-id # get equipment
* DELETE /api/v1/equipment/:equipment-id # delete equipment



### release_application related

* GET /api/v1/equipment-application/:equipment-application-id # get application
* POST /api/v1/equipment-application/ # create a new equipment application
* PUT /api/v1/equipment-application/:equipment-application-id # edit application status
  * status
* DELETE /api/v1/equipment-application/:equipment-application-id # delete equipment application



### renter_application related

* POST /api/v1/renter-application/ # create a new renter application
* PUT /api/v1/renter-application/:renter-application-id # edit application status
  * status
* DELETE /api/v1/equipment-application/:renter-application-id # delete renter application



### rent_application related

* GET /api/v1/rent-application/ # 获取所有的申请
* GET /api/v1/rent-application/userId/:userId # 获取某一用户的申请
* GET /api/v1/rent-application/:rent-application-id # 获取某一申请
* POST /api/v1/rent-application/ # create a new rent application
* PUT /api/v1/rent-application/:rent-application-id/approve  # edit application status
  * status
* DELETE /api/v1/equipment-application/:rent-application-id # delete rent application



改变application status时应该注意

* 同步更新用户、设备提供者状态

	* 提示用户、设备提供者