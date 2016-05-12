% include('head.inc.tpl', title='Page Title')
    <!-- Page Content -->
    <div class="container">

            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">Firms</h1>
                </div>
                <!-- /.col-lg-12 -->
                <div class="col-lg-12">
                    <h3 class="panel-body"> Add new firm</h3>
                    <form method="POST" action="/etc">
                     <input name="name" type="input" placeholder="name">
                     <input name="representative" type="input" placeholder="representative">
                     <input name="phone" type="input" placeholder="phone">
                     <input name="mail" type="input" placeholder="mail">
                     <input type="submit" value="Submit">
                    </form>
                </div>
            </div>
            <!-- /.row -->
    </div>
    <!-- /.container -->
% include('foot.inc.tpl')