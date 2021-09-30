#include "InfoWidget.h"

#include "ui_InfoWidget.h"

InfoWidget::InfoWidget(QWidget *parent) : QWidget(parent),
                                          ui(new Ui::InfoWidget) {
    ui->setupUi(this);

    this->setWindowFlags(Qt::WindowType::Dialog | Qt::WindowType::WindowMinimizeButtonHint);

    connect(ui->btn_start, &QPushButton::clicked, this, &InfoWidget::signal_startClicked);
    connect(ui->btn_stop, &QPushButton::clicked, this, &InfoWidget::signal_stopClicked);
    connect(ui->widgetList, &QListWidget::currentRowChanged, this, &InfoWidget::signal_widgetSelected);
    connect(ui->widgetList, &QListWidget::currentRowChanged, this, &InfoWidget::slot_onWidgetSelected);
    connect(ui->attrTable, &QTableWidget::itemChanged, this, &InfoWidget::slot_onAttrModified);
}

InfoWidget::~InfoWidget() {
    delete ui;
}

void InfoWidget::slot_onWidgetChanged(const std::vector<QWidget *> &widgets) {
    ui->widgetList->clear();
    int row = 0;
    for (auto const &w : widgets) {
        ui->widgetList->insertItem(row, new QListWidgetItem(w->objectName(), ui->widgetList));
        row++;
    }
    m_widgets = widgets;
    m_selected = nullptr;
}

static inline QTableWidgetItem *CreateROItem(const QString &text) {
    auto nameItem = new QTableWidgetItem(text);
    nameItem->setFlags(nameItem->flags() & ~Qt::ItemIsEditable);
    return nameItem;
}

void InfoWidget::slot_onWidgetSelected(const int &index) {
    ui->attrTable->setRowCount(0);
    if (0 <= index && (size_t)index < m_widgets.size()) {
        m_selected = m_widgets.at(index);
        auto const &names = m_selected->dynamicPropertyNames();
        int row = 0;
        foreach (auto const &name, names) {
            ui->attrTable->insertRow(row);
            ui->attrTable->setItem(row, 0, CreateROItem(QString::fromUtf8(name)));
            auto prop = m_selected->property(name.data());
            if (prop.canConvert<QString>()) {
                ui->attrTable->setItem(row, 1, new QTableWidgetItem(prop.toString()));
            } else {
                ui->attrTable->setItem(row, 1, CreateROItem("prop is not string"));
            }
            ++row;
        }

        // add attributes here
        {
            ui->attrTable->insertRow(row);
            ui->attrTable->setItem(row, 0, CreateROItem("styleSheet"));
            auto const styleSheet = m_selected->styleSheet();
            ui->attrTable->setItem(row, 1, new QTableWidgetItem(styleSheet));
            ++row;
        }
    }
}

void InfoWidget::slot_onAttrModified(QTableWidgetItem *item) {
    if (item->column() == 0) return;

    auto row = item->row();
    auto attrName = ui->attrTable->item(row, 0);

    // add attributes here
    if (attrName->text() == "styleSheet") {
        m_selected->setStyleSheet(item->text());
    } else {
        auto name = attrName->text().toUtf8();
        m_selected->setProperty(name.data(), item->text());
    }
}
