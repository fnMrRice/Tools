#include "TestWidget.h"

#include "include/WidgetModifier.h"
#include "ui_TestWidget.h"

TestWidget::TestWidget(QWidget *parent)
    : QWidget(parent), ui(new Ui::TestWidget) {
    ui->setupUi(this);

    m_modifier = new WidgetModifier(this, nullptr);
}

TestWidget::~TestWidget() {
    delete ui;
}
