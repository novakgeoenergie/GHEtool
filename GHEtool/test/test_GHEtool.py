# test if model can be imported
from GHEtool import *
import pytest
import numpy as np
import pygfunction as gt

data = GroundData(110, 6, 3, 10, 0.2, 10, 12)
fluidData = FluidData(0.2, 0.568, 998, 4180, 1e-3)
pipeData = PipeData(1, 0.015, 0.02, 0.4, 0.05, 0.075, 2)

# Monthly loading values
peakCooling = [0., 0, 34., 69., 133., 187., 213., 240., 160., 37., 0., 0.]              # Peak cooling in kW
peakHeating = [160., 142, 102., 55., 0., 0., 0., 0., 40.4, 85., 119., 136.]             # Peak heating in kW

# annual heating and cooling load
annualHeatingLoad = 300*10**3 # kWh
annualCoolingLoad = 160*10**3 # kWh

# percentage of annual load per month (15.5% for January ...)
montlyLoadHeatingPercentage = [0.155, 0.148, 0.125, .099, .064, 0., 0., 0., 0.061, 0.087, 0.117, 0.144]
montlyLoadCoolingPercentage = [0.025, 0.05, 0.05, .05, .075, .1, .2, .2, .1, .075, .05, .025]

# resulting load per month
monthlyLoadHeating = list(map(lambda x: x * annualHeatingLoad, montlyLoadHeatingPercentage))   # kWh
monthlyLoadCooling = list(map(lambda x: x * annualCoolingLoad, montlyLoadCoolingPercentage))   # kWh

custom_field = gt.boreholes.L_shaped_field(N_1=4, N_2=5, B_1=5., B_2=5., H=100., D=4, r_b=0.05)


def test_borefield():
    borefield = Borefield(simulation_period=20,
                          peak_heating=peakHeating,
                          peak_cooling=peakCooling,
                          baseload_heating=monthlyLoadHeating,
                          baseload_cooling=monthlyLoadCooling)

    borefield.set_ground_parameters(data)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature

    assert borefield.simulation_period == 20
    assert borefield.Tf_C == 0
    assert borefield.Tf_H == 16
    np.testing.assert_array_equal(borefield.peak_heating, np.array([160., 142, 102., 55., 26.301369863013697, 0., 0., 0., 40.4, 85., 119., 136.]))


@pytest.fixture
def borefield():
    borefield = Borefield(simulation_period=20,
                          peak_heating=peakHeating,
                          peak_cooling=peakCooling,
                          baseload_heating=monthlyLoadHeating,
                          baseload_cooling=monthlyLoadCooling)

    borefield.set_ground_parameters(data)

    # set temperature boundaries
    borefield.set_max_ground_temperature(16)  # maximum temperature
    borefield.set_min_ground_temperature(0)  # minimum temperature
    return borefield


@pytest.fixture
def empty_borefield():
    borefield = Borefield()
    return borefield


@pytest.fixture
def hourly_borefield():
    borefield = Borefield()
    borefield.set_ground_parameters(data)
    borefield.load_hourly_profile("./Examples/hourly_profile.csv")
    return borefield


@pytest.fixture
def borefield_cooling_dom():
    borefield = Borefield(simulation_period=20,
                          peak_heating=peakHeating,
                          peak_cooling=peakCooling,
                          baseload_heating=monthlyLoadHeating,
                          baseload_cooling=monthlyLoadCooling)

    borefield.set_baseload_cooling(np.array(monthlyLoadCooling)*2)

    borefield.set_ground_parameters(data)
    return borefield


def test_empty_values(empty_borefield):
    np.testing.assert_array_equal(empty_borefield.baseload_cooling, np.zeros(12))


def test_size(borefield):
    assert borefield.size(100) == 91.94137647834752


def test_imbalance(borefield):
    assert borefield.imbalance == -140000.0


def test_temperatureProfile(borefield):
    borefield.calculate_temperatures(depth=90)
    np.testing.assert_array_equal(np.around(borefield.results_peak_cooling, 8),
                                  np.around(np.array([9.072138635889608, 9.164501691326635, 9.77185417804152, 10.722355031147949, 12.541710006586252, 14.381247642479014, 15.34715523270872, 16.133256617527323, 13.594996056819344, 10.321836077321088, 9.352436886779245, 8.8637583612847, 8.649554750391617, 8.7584081060008, 9.378240559263338, 10.3381322568525, 12.164941284401, 14.013767343409306, 14.986897869588127, 15.778632202274398, 13.247637721629822, 9.980587317784186, 9.018928749684388, 8.536692466498353, 8.327133427706803, 8.443947159711584, 9.067315947096022, 10.031098727159772, 11.867870299100604, 13.721443658583802, 14.699864573062309, 15.495636956390392, 12.964877330686557, 9.7009776067226, 8.74407425656506, 8.264961111806505, 8.062971415184636, 8.185007964800743, 8.811799143255827, 9.781535764723834, 11.618692184652073, 13.473287790618429, 14.45574423216039, 15.255737457847333, 12.728975947127138, 9.470123974992791, 8.513128144510613, 8.036370994221016, 7.838074304448629, 7.963675888518237, 8.59527057680676, 9.566716807689438, 11.4040187879261, 13.261621088094032, 14.247312288215454, 15.050095793662155, 12.530047598907084, 9.273023799018986, 8.318687246223682, 7.845848533043945, 7.650836230485071, 7.7779392859426, 8.407331136302897, 9.3743988337209, 11.211533338801281, 13.070899048337175, 14.06011556769677, 14.87229180129198, 12.358409743892787, 9.10602954077039, 8.155238188915366, 7.684141553519941, 7.487890386649131, 7.611071788027462, 8.235782023542598, 9.20155704613557, 11.040193916692203, 12.902906900677749, 13.899620545542387, 14.718477090644532, 12.208629728475143, 8.95939799664649, 8.010440838795109, 7.538941665799753, 7.339870476522034, 7.459171356963437, 8.081887061197177, 9.048589820662093, 10.889651352331544, 12.75732457338642, 13.760848354345358, 14.583272517197944, 12.076264094587364, 8.82891272068688, 7.880143057992938, 7.406624015057043, 7.204272503072776, 7.321107061091576, 7.944338573602958, 8.912795238487599, 10.756957636327195, 12.63143561991673, 13.638141198095932, 14.463142161206784, 11.958021857423834, 8.711281514500218, 7.761097277187296, 7.284775956173105, 7.079650968634789, 7.196696849130592, 7.821174031828835, 8.79201403661828, 10.643368351032697, 12.522116310928723, 13.532329499879989, 14.359976164672524, 11.856020202389194, 8.608025439970287, 7.6546011879292974, 7.174655022851516, 6.968965593092257, 7.087324858868631, 7.714559157548115, 8.68954856913047, 10.541845715416905, 12.420593675312933, 13.430806864264197, 14.258453529056734, 11.7544975667734, 8.506502804354493, 7.553078552313505, 7.073132387235724, 6.867442957476465, 6.985802223252841, 7.614705713718261, 8.59431016871427, 10.450494157361314, 12.332305449943693, 13.344427862572113, 14.171985775025211, 11.665573788905736, 8.413923782041604, 7.458191421514392, 6.97897142332109, 6.775403161956499, 6.897333191592656, 7.5291747725503315, 8.508779227546341, 10.364963216193388, 12.246774508775765, 13.258896921404187, 14.086454833857282, 11.580042847737808, 8.328392840873676, 7.372660480346462, 6.89344048215316, 6.689872220788571, 6.815222693844942, 7.450373833259667, 8.432677979415317, 10.290872205136514, 12.173457009760323, 13.184356110859632, 14.009195553248034, 11.499922019692043, 8.248170964434062, 7.293593953684344, 6.816681078111735, 6.616510010094435, 6.742211022711779, 7.377362162126503, 8.359666308282153, 10.217860534003352, 12.10044533862716, 13.111344439726468, 13.936183882114875, 11.426910348558877, 8.175159293300897, 7.22058228255118, 6.745061256386194, 6.547741618446253, 6.675829924479988, 7.312843511330983, 8.296230698758595, 10.15418204786456, 12.035094174535725, 13.043695900460184, 13.867361272019181, 11.358639305198231, 8.10832627304841, 7.156091119613595, 6.682100601643008, 6.484780963703065, 6.6128692697368034, 7.249882856587797, 8.23327004401541, 10.091221393121375, 11.97213351979254, 12.980735245716994, 13.804400617275993, 11.295678650455043, 8.045396218406552, 7.095638681175832, 6.623768962227816, 6.428166513973984, 6.557511664169497, 7.194929028357508, 8.177370292652899, 10.033452835570712, 11.912520852135497, 12.92126539453286, 13.745763568849506, 11.238632959297998, 7.990611590736534, 7.040854053505812, 6.568984334557799, 6.373381886303969, 6.502727036499478, 7.140144400687494, 8.122585664982886, 9.978668207900697, 11.85773622446548, 12.866480766862844, 13.690978941179491, 11.185576299647401, 7.940346475055395, 6.992911689336418, 6.522834648422105, 6.328194620796975, 6.457111440663307, 7.092733971450005, 8.072886627216201, 9.928075133441668, 11.807787408982822, 12.818068924436947, 13.644997226761404, 11.140804334292604, 7.895574509700595, 6.948139723981622, 6.478062683067304]), 8))


def test_quadrantSizing(borefield):
    assert round(borefield.size(100, quadrant_sizing=3), 2) == 41.27


def test_dynamicRb(borefield):
    borefield.set_fluid_parameters(fluidData)
    borefield.set_pipe_parameters(pipeData)
    assert round(borefield.size(100, use_constant_Rb=False), 2) == 52.57


def test_load_custom_configuration(borefield):

    borefield.set_borefield(custom_field)
    assert borefield.borefield == custom_field


def test_load_custom_gfunction(borefield):
    borefield.set_custom_gfunction("customfield")


def test_simulation_period(borefield):
    borefield.set_simulation_period(25)
    assert borefield.simulation_period == 25


def test_without_pipe(borefield):
    borefield.set_pipe_parameters(pipeData)
    borefield.set_fluid_parameters(fluidData)


def test_Tg(borefield):
    borefield.use_constant_Tg = False
    borefield._Tg()


def test_calculate_Rb(borefield):
    try:
        borefield.calculate_Rb()
    except ValueError:
        assert True


def test_to_small_field(borefield):
    borefield.H = 0.5
    borefield._Carcel


def test_too_much_sizing_methods(borefield):
    try:
        borefield.sizing_setup(L2_sizing=True, L3_sizing=True)
    except ValueError:
        assert True


def test_size_L3(borefield):
    borefield.size(L3_sizing=True)


def test_size_L4(hourly_borefield):
    hourly_borefield.size(L4_sizing=True)


def test_cooling_dom(borefield_cooling_dom):
    borefield_cooling_dom.size()


def test_sizing_different_quadrants(borefield):
    borefield.size(quadrant_sizing=1)
    borefield.size(quadrant_sizing=2)
    borefield.size(quadrant_sizing=3)
    borefield.size(quadrant_sizing=4)
    borefield.size(quadrant_sizing=1, L3_sizing=True)


def test_convergence(borefield_cooling_dom):
    try:
        borefield_cooling_dom.set_peak_heating(np.array(peakHeating)*15)
        borefield_cooling_dom.size()
    except RuntimeError:
        assert True


def test_quadrant_4(borefield):
    borefield.set_peak_heating(np.array(peakHeating)*8)
    borefield.size()


def test_sizing_L3(borefield):
    borefield.set_peak_heating(np.array(peakHeating)*8)
    borefield.size(L3_sizing=True)


def test_sizing_L32(borefield_cooling_dom):
    borefield_cooling_dom.size(L3_sizing=True)
    borefield_cooling_dom.set_peak_heating(np.array(peakHeating) * 5)
    borefield_cooling_dom.size(L3_sizing=True)


def test_size_L4(borefield):
    try:
        borefield.size(L4_sizing=True)
    except ValueError:
        assert True