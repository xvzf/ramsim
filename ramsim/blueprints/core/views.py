from flask import render_template, url_for, redirect, request, abort

from . import blueprint
from .forms import ProcessForm

from .ramsim_runner import RamsimRunner


@blueprint.errorhandler(404)
def page_not_found(e):
    return render_template("core/404.html"), 404

@blueprint.route("/", methods=["GET", "POST"])
def index():
    form = ProcessForm()

    if form.validate_on_submit():
        # Process
        uuid = RamsimRunner.add_to_db_and_exec(form.code.data, form.svar.data)
        return redirect(url_for(".process", uuid=uuid))

    return render_template("core/index.html", form=form)


@blueprint.route("/<uuid>", methods=["GET"])
def process(uuid):
    uuid_dict = RamsimRunner.get_code_svars_from_uuid(uuid)

    if not uuid_dict:
        return abort(404)
    
    return render_template("core/uuid.html", svars=uuid_dict["svars"],   code=uuid_dict["code"],
                                             result=uuid_dict["result"], error=uuid_dict["error"],
                                             csvurl=url_for("static", filename=f"code/{uuid}.ramsim.csv"),
                                             errors=uuid_dict["errors"], exectable=uuid_dict["exectable"])