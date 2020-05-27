# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardAddMedicalMessage(models.TransientModel):

    _inherit = "wizard.add.medical.message"

    procedure_item_ids = fields.One2many(
        "wizard.add.medical.message.procedure", inverse_name="wizard_id"
    )

    questionnaire_item_ids = fields.One2many(
        "wizard.add.medical.message.questionnaire", inverse_name="wizard_id"
    )

    questionnaire_item_response_ids = fields.One2many(
        "wizard.add.medical.message.questionnaire.item",
        inverse_name="wizard_id",
    )

    @api.onchange("questionnaire_item_ids", "questionnaire_item_ids.done")
    def on_change_questionnaire_item_ids(self):
        self.questionnaire_item_response_ids = [(6, 0, [])]
        values = []
        for pr in self.questionnaire_item_ids.filtered("done").mapped(
            "procedure_request_id"
        ):
            values += [
                (
                    0,
                    0,
                    self.careplan_medical_id._action_add_message_element_questionnaire_item_vals(
                        pr, question
                    ),
                )
                for question in pr.questionnaire_id.item_ids
            ]
        print(values)
        self.questionnaire_item_response_ids = values

    def _get_careplan_message_kwargs(self):
        result = super()._get_careplan_message_kwargs()
        result["procedure_request_ids"] = (
            self.procedure_item_ids.filtered(lambda r: r.done)
            .mapped("procedure_request_id")
            .ids
        )
        # TODO: probablemente no es el sitio a procesar esto
        questionnaire_response_ids = self.process_questionnaire_items()
        result["questionnaire_response_ids"] = questionnaire_response_ids.ids
        return result

    def process_questionnaire_items(self):
        responses = self.env["medical.questionnaire.response"]
        for pr in self.questionnaire_item_ids.filtered("done").mapped(
            "procedure_request_id"
        ):
            vals = []
            for item in self.questionnaire_item_response_ids:
                if item.procedure_request_id == pr.id:
                    # item_vals = item.copy_vals()
                    vals.append(
                        (0, 0, {"name": item.name, "result": item.result})
                    )
            responses |= self.env["medical.questionnaire.response"].create(
                {
                    "medical_careplan_id": self.careplan_medical_id.id,
                    "procedure_request_id": pr.id,
                    "item_ids": vals,
                }
            )
        return responses


class WizardAddMedicalMessageProcedure(models.TransientModel):
    _name = "wizard.add.medical.message.procedure"
    _description = "Procedure in medical message"

    wizard_id = fields.Many2one("wizard.add.medical.message")
    procedure_request_id = fields.Many2one(
        "medical.procedure.request", required=True, readonly=True
    )
    name = fields.Char(compute="_compute_name")
    done = fields.Boolean()

    @api.depends("procedure_request_id")
    def _compute_name(self):
        for record in self:
            record.name = (
                record.procedure_request_id.service_id.display_name
                or record.procedure_request_id.name
            )


class WizardAddMedicalMessageQuestionnaireItem(models.TransientModel):
    _name = "wizard.add.medical.message.questionnaire.item"
    _inherit = "medical.questionnaire.item.abstract"
    _description = "Questionnaire in medical message"

    wizard_id = fields.Many2one("wizard.add.medical.message")


class WizardAddMedicalMessageQuestionnaire(models.TransientModel):
    _name = "wizard.add.medical.message.questionnaire"
    _description = "Questionnaire in medical message"

    wizard_id = fields.Many2one("wizard.add.medical.message")
    procedure_request_id = fields.Many2one(
        "medical.procedure.request", required=True, readonly=True
    )
    name = fields.Char(compute="_compute_name")
    done = fields.Boolean()

    @api.depends("procedure_request_id")
    def _compute_name(self):
        for record in self:
            record.name = (
                record.procedure_request_id.service_id.display_name
                or record.procedure_request_id.name
            )
