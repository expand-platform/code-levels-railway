const DOM = {
    timeline: "timeline",
    timelineStepper: "timeline__stepper",
    timelineStep: "timeline__step",
    timelineStepTitle: "timeline__step-title",
    timelineStepActive: "is-active",
    timelineStepActiveMarker: "timeline__step-active-marker",
    timelineSlidesContainer: "timeline__slides",
    timelineSlide: "timeline__slide",
    timelineSlideActive: "is-active",
};

const STEP_ACTIVE_MARKEP_CUSTOM_PROPS = {
    width: "--slide-width",
    posX: "--slide-pos-x",
    posY: "--slide-pos-y",
};

const SLIDES_CONTAINER_CUSTOM_PROPS = {
    height: "--slides-container-height",
};

const timeline = document.querySelector(`.${DOM.timeline}`);
const timelineStepper = timeline?.querySelector(`.${DOM.timelineStepper}`);
const timelineStepTitle = timeline?.querySelector(`.${DOM.timelineStepTitle}`);
const timelineSlidesContainer = timeline?.querySelector(
    `.${DOM.timelineSlidesContainer}`
);
const timelineSlides =
    timeline && Array.from(timeline.querySelectorAll(`.${DOM.timelineSlide}`));



window.addEventListener("load", () => {
    createStepActiveMarker();
    activateCurrentSlide();
});

window.addEventListener("resize", () => {
    recalcStepActiveMarkerProps();
});

timeline?.addEventListener("click", (event) => {
    const { target } = event;

    if (
        !target ||
        !(target instanceof Element) ||
        !target.closest(`.${DOM.timelineStep}`)
    ) {
        return;
    }

    const currentStep = target.closest(`.${DOM.timelineStep}`);

    if (!currentStep) {
        return;
    }

    deactivateSteps();
    activateCurrentStep(currentStep);

    recalcStepActiveMarkerProps();

    deactivateSlides();
    activateCurrentSlide();
});

function deactivateSteps() {
    const steps = document.querySelectorAll(`.${DOM.timelineStep}`);
    steps?.forEach((elem) => elem.classList.remove(`${DOM.timelineStepActive}`));
}

function activateCurrentStep(currentStep) {
    currentStep?.classList.add(`${DOM.timelineStepActive}`);
}

function deactivateSlides() {
    timelineSlides?.forEach((elem) =>
        elem.classList.remove(`${DOM.timelineSlideActive}`)
    );
}

function activateCurrentSlide() {
    const currentSlide = getCurrentSlide();

    if (!currentSlide) {
        return;
    }

    const currentSlideHeight = getCurrentSlideHeight(currentSlide);
    setSlideContainerHeight(currentSlideHeight);
    currentSlide.classList.add(`${DOM.timelineSlideActive}`);
}

function createStepActiveMarker() {
    const stepActiveMarker = document.createElement("div");
    stepActiveMarker.classList.add(`${DOM.timelineStepActiveMarker}`);
    timelineStepper?.appendChild(stepActiveMarker);

    const positionProps = getStepActiveMarkerProps();

    if (!positionProps) {
        return;
    }

    setStepActiveMarkerProps({
        stepActiveMarker,
        ...positionProps,
    });
}

function recalcStepActiveMarkerProps() {
    const stepActiveMarker = timeline?.querySelector(
        `.${DOM.timelineStepActiveMarker}`
    );

    const stepActiveMarkerProps = getStepActiveMarkerProps();
    if (!stepActiveMarkerProps) {
        return;
    }

    setStepActiveMarkerProps({ stepActiveMarker, ...stepActiveMarkerProps });
}

function setStepActiveMarkerProps({
    stepActiveMarker,
    posX,
    posY,
    width,
}) {
    stepActiveMarker.style.setProperty(
        `${STEP_ACTIVE_MARKEP_CUSTOM_PROPS.width}`,
        `${width}px`
    );

    stepActiveMarker.style.setProperty(
        `${STEP_ACTIVE_MARKEP_CUSTOM_PROPS.posX}`,
        `${posX}px`
    );

    if (typeof posY === "number") {
        stepActiveMarker.style.setProperty(
            `${STEP_ACTIVE_MARKEP_CUSTOM_PROPS.posY}`,
            `${posY}px`
        );
    }
}

function getStepActiveMarkerProps() {
    const { currentStep } = getCurrentStep();

    if (!currentStep) {
        return null;
    }

    const width = getElementWidth(currentStep);
    const posX = getStepActiveMarkerPosX(currentStep);
    const posY = getStepActiveMarkerPosY();

    if (typeof posX !== "number" || typeof posY !== "number") {
        return null;
    }

    return { posX, posY, width };
}

function getCurrentStep() {
    const timelineSteps = Array.from(
        document.querySelectorAll(`.${DOM.timelineStep}`)
    );
    console.log('- timelineSteps -', timelineSteps);

    const currentStep = timelineSteps.find((element) =>
        element.classList.contains(`${DOM.timelineStepActive}`)
    );

    const currentStepIndex =
        currentStep &&
        timelineSteps.findIndex((element) =>
            element.classList.contains(`${DOM.timelineStepActive}`)
        );

    return { currentStep, currentStepIndex };
}

function getCurrentSlide() {
    const { currentStepIndex } = getCurrentStep();

    if (typeof currentStepIndex !== "number" || !timelineSlides) {
        return null;
    }

    return timelineSlides[currentStepIndex];
}

function setSlideContainerHeight(height) {
    timelineSlidesContainer?.style.setProperty(
        `${SLIDES_CONTAINER_CUSTOM_PROPS.height}`,
        `${height}px`
    );
}

function getCurrentSlideHeight(currentSlide) {
    return currentSlide.clientHeight;
}

function getStepActiveMarkerPosY() {
    const timelineTitlePosY = timelineStepTitle?.getBoundingClientRect().top;
    const timelineStepperPosY = timelineStepper?.getBoundingClientRect().top;

    if (!timelineTitlePosY || !timelineStepperPosY) {
        return null;
    }

    return timelineTitlePosY - timelineStepperPosY;
}

function getStepActiveMarkerPosX(currentStep) {
    const timelineStepperPosX = timelineStepper?.getBoundingClientRect().left;
    const currentStepPosX = currentStep.getBoundingClientRect().left;

    if (!timelineStepperPosX) {
        return null;
    }

    return currentStepPosX - timelineStepperPosX;
}

function getElementWidth(elem) {
    return elem.clientWidth;
}
