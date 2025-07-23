document.querySelectorAll('[data-modal]').forEach((modal) => {
    const modalBox = modal.querySelector('[data-modal-box]');
    const closeModalBtn = modal.querySelector('[data-close-modal]');
    const chooseTemplateBtn = modal.querySelector('[data-choose-template]');
    const backBtn = modal.querySelector('[data-back]');
    const showModalBtn = document.querySelector(`[data-show-modal="${modal.dataset.modal}"]`);

    let isModalOpen = false;

    // Этапы
    const step1 = modal.querySelector('.step1');
    const step2 = modal.querySelector('.step2');

    // Открытие модального окна на первом этапе
    showModalBtn.addEventListener('click', (e) => {
        modal.classList.add('active');
        step1.classList.add('active');
        step2.classList.remove('active');
        isModalOpen = true;
        e.stopPropagation();
    });

    // Переход ко второму этапу
    chooseTemplateBtn.addEventListener('click', (e) => {
        step1.classList.remove('active');
        step2.classList.add('active');
        isModalOpen = true;
        e.stopPropagation();
    });

    // Возврат к первому этапу
    backBtn.addEventListener('click', (e) => {
        step2.classList.remove('active');
        step1.classList.add('active');
        isModalOpen = true;
        e.stopPropagation();
    });

    // Закрытие модального окна
    closeModalBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        isModalOpen = false;
    });

    // Закрытие модального окна при клике вне его
    document.addEventListener('click', (e) => {
        if (isModalOpen && !modalBox.contains(e.target)) {
            modal.classList.remove('active');
            isModalOpen = false;
        }
    });
});
