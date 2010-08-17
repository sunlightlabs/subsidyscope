
SECTORS = { 'sector': 'home',
            'name': 'SubsidyScope',
            'url_name': 'index',
            'children': [{ 'sector': 'home',
                           'name': 'Home',
                           'url_name': 'index',
                           'children': []
                         },
                         { 'sector': 'bailout-index',
                           'name': 'Financial Bailout',
                           'url_name': 'bailout-index',
                           'children': [{ 'sector': 'bailout-index',
                                          'name': 'Treasury',
                                          'url_name': 'bailout_treasury_index',
                                          'children': [ { 'sector': 'bailout_treasury_index',
                                                          'name': 'Overview',
                                                          'url_name': 'bailout_treasury_index',
                                                          'children': []
                                                        },
                                                        { 'sector':'bailout_treasury_index',
                                                          'name': 'Fannie Mae and Freddie Mac',
                                                          'url_name': 'fannie_freddie_index',
                                                          'children' : []
                                                        },
                                                        { 'sector': 'bailout_treasury_index',
                                                        'name': 'TARP Disbursements',
                                                        'url_name': 'tarp',
                                                        'children': []
                                                        },
                                                        { 'sector': 'bailout_treasury_index',
                                                        'name': 'TARP Map',
                                                        'url_name': 'tarp-map',
                                                        'children': [],
                                                        },
                                                        { 'sector':'bailout_treasury_index',
                                                        'name': 'TARP Subsidies',
                                                        'url_name': 'tarp-subsidies',
                                                        'children': [{ 'sector': 'tarp',
                                                                        'name': 'COP Estimates',
                                                                        'url_name': 'tarp-subsidies-cop',
                                                                        'children': []
                                                                    },
                                                                    { 'sector': 'tarp',
                                                                        'name': 'CBO Estimates',
                                                                        'url_name': 'tarp-subsidies-cbo',
                                                                        'children': []
                                                                    }]
                                                        }, 
                                                        { 'sector': 'bailout_treasury_index',
                                                        'name': 'TARP Warrants',
                                                        'url_name': 'tarp-warrants',
                                                        'children': [{ 'sector': 'tarp-warrants',
                                                                        'name': 'Inconsistencies in Warrant Policy',
                                                                        'url_name': 'tarp-warrants-calculation',
                                                                        'children': []
                                                                    }]
                                                        }],
                                        },
                                        { 'sector': 'bailout-index',
                                          'name': 'FDIC',
                                          'url_name': 'bailout_fdic_index',
                                          'children': [{ 'sector': 'bailout_fdic_index',
                                                         'name': 'Overview',
                                                         'url_name': 'bailout_fdic_index',
                                                         'children': []
                                                       },
                                                       { 'sector': 'bailout_fdic_index',
                                                         'name': 'Bank Failures and the Deposit Insurance Fund',
                                                         'url_name': 'fdic_bank_failures',
                                                         'children': [{ 'sector': 'fdic_bank_failures',
                                                                        'name': 'Bank Failures Table',
                                                                        'url_name': 'fdic_bank_failures_table',
                                                                        'children': []
                                                                      },    
                                                                      { 'sector': 'fdic_bank_failures',
                                                                        'name': 'Prepayment Requirement',
                                                                        'url_name': 'fdic_bank_failures_prepayment_requirement',
                                                                        'children': []
                                                                      }]
                                                        },
                                                        { 'sector': 'bailout_fdic_index',
                                                          'name': 'Legacy Loan Program Comments',
                                                          'url_name': 'fdic_llp_comments',
                                                          'children': []
                                                        },
                                                        { 'sector': 'bailout_fdic_index',
                                                          'name': 'TLGP Monthly Reports',
                                                          'url_name': 'fdic_tlgp',
                                                          'children':[]
                                                        }]
                                        },
                                        { 'sector': 'bailout-index',
                                          'name': 'Federal Reserve',
                                          'url_name': 'bailout_federal_reserve_index',
                                          'children': []
                                        },
                                        { 'sector': 'bailout-index',
                                          'name': 'Other Agencies',
                                          'url_name': 'bailout_other_index',
                                          'children': [{ 'sector': 'bailout_other_index',
                                                         'name': 'Overview',
                                                         'url_name': 'bailout_other_index',
                                                         'children': []
                                                       },
                                                       { 'sector': 'bailout_other_index',
                                                         'name': 'Federal Home Loan Banks',
                                                         'url_name': 'fhlb_index',
                                                         'children': []
                                                       }]
                                        },
                                        { 'sector': 'bailout-index',
                                          'name': 'Key Documents',
                                          'url_name': 'bailoutpdf_index',
                                          'children': []
                                        }],
                        },
                        { 'sector':'transportation-index',
                          'name': 'Transportation',
                          'url_name':'transportation-index',
                          'children': [{'sector': 'transportation-index',
                                        'name': 'Summary',
                                        'url_name': 'transportation-overview',
                                        'children': [{'sector': 'transportation-overview',
                                                      'name': 'Aviation',
                                                      'url_name': 'transportation-aviation',
                                                      'children':[]
                                                    },
                                                    {'sector': 'transportation-overview',
                                                     'name': 'Highways', 
                                                     'url_name':'transportation-highways',
                                                     'children': []
                                                    },
                                                    {'sector': 'transportation-overview',
                                                     'name': 'Maritime',
                                                     'url_name': 'transportation-maritime',
                                                     'children':[]
                                                    },
                                                    {'sector': 'transportation-overview',
                                                     'name': 'Rail',
                                                     'url_name':'transportation-rail',
                                                     'children': []
                                                    },
                                                    {'sector': 'transportation-overview',
                                                     'name': 'Transit',
                                                     'url_name': 'transportation-transit',
                                                     'children': []
                                                    }]
                                        },
                                        {'sector': 'transportation-index',
                                         'name': 'Grants and Contracts',
                                         'url_name': 'transportation-direct-expenditures',
                                         'children': [{ 'sector': 'transportation-direct-expenditures',
                                                        'name': 'Direct Expenditures Program Directory (CFDA)',
                                                        'url_name': 'transportation-cfdaprograms-index',
                                                        'children': []
                                                      },
                                                      { 'sector': 'transportation-direct-expenditures',
                                                        'name': 'Search Direct Expenditures',
                                                        'url_name': 'transportation-faads-search',
                                                        'children':[]
                                                      },
                                                      { 'sector': 'transportation-direct-expenditures',
                                                        'name': 'Airport Improvement Program (AIP)',
                                                        'url_name': 'aip-story',
                                                        'children': [{ 'sector': 'aip-story',
                                                                       'name': 'Analysis',
                                                                       'url_name': 'aip-story',
                                                                       'children':[]
                                                                     },
                                                                     { 'sector': 'aip-story',
                                                                       'name': 'Grant Search',
                                                                       'url_name': 'aip-index',
                                                                       'children': []
                                                                     }, 
                                                                     {'sector':'aip-story', 
                                                                        'name': 'Airport Detail', 
                                                                        'url_name': 'aip.views.portdata',
                                                                        'url_pattern': '.*/transportation/aip/airports/.*', 
                                                                        'children': [], 
                                                                        'hide': True
                                                                     }]
                                                      },
                                                      {'sector': 'transportation-direct-expenditures',
                                                       'name': 'Amtrak',
                                                       'url_name': 'transportation-amtrak',
                                                       'children': [{ 'sector': 'transportation-amtrak',
                                                                      'name': 'Analysis',
                                                                      'url_name': 'transportation-amtrak',
                                                                      'children': []
                                                                    },
                                                                    { 'sector': 'transportation-direct-expenditures',
                                                                      'name': 'Route Performance Table',
                                                                      'url_name': 'transportation-amtrak-table',
                                                                      'children': []
                                                                    }]
                                                      },
                                                      {'sector': 'transportation-direct-expenditures',
                                                       'name': 'Highway Funding Analysis',
                                                       'url_name': 'transportation-highway-funding',
                                                       'children': []
                                                      }]
                                        },
                                        {'sector': 'transportation-index',
                                         'name': 'Tax Subsidies',
                                         'url_name': 'transportation-tax-expenditures',
                                         'children': [{ 'sector': 'transportation-tax-expenditures',
                                                        'name': 'Employer-paid Transportation Benefits',
                                                        'url_name': 'transportation-tax-expenditures-employer-paid-benefits',
                                                        'children':[]
                                                      },
                                                      {'sector': 'transportation-tax-expenditures',
                                                       'name': 'Tax Credit for Certain Expenditures for Maintaining Tracks',
                                                       'url_name': 'transportation-tax-expenditures-track-maintenance',
                                                       'children':[]
                                                      },
                                                      {'sector': 'transportation-tax-expenditures',
                                                       'name': 'Exclusion of Interest on Bonds for Financing of Highway Project and Rail-Truck Transfer Facilities',
                                                       'url_name': 'transportation-tax-expenditures-bond-interest-exclusion',
                                                       'children':[]
                                                      },
                                                      {'sector': 'transportation-tax-expenditures',
                                                       'name': 'Deferral of Tax on Shipping Companies',
                                                       'url_name': 'transportation-tax-expenditures-capital-construction-funds',
                                                       'children':[]
                                                      }]
                                        },
                                        {'sector': 'transportation-index',
                                         'name': 'Loans and Loan Guarantees',
                                         'url_name': 'transportation-risk-transfers',
                                         'children': [{'sector': 'transportation-risk-transfers',
                                                       'name': 'Export/Import Bank',
                                                       'url_name': 'transportation-exim',
                                                       'children': []
                                                      }]
                                        },
                                       # {'sector': 'transportation-index',
                                       #  'name': 'Contracts',
                                       #  'url_name': 'transportation-contracts',
                                       #  'children':[]
                                       #}
                                        ]
                         },
                        { 'sector': 'nonprofits-index',
                          'name': 'Nonprofits',
                          'url_name': 'nonprofits-index',
                          'children':[{'sector': 'nonprofits-index',
                                       'name': 'Summary',
                                       'url_name': 'nonprofits-overview',
                                       'children': [{'sector': 'nonprofits-overview',
                                                      'name': 'Structure of Nonprofit Sector in the U.S.',
                                                      'url_name': 'nonprofits-overview-structure',
                                                      'children':[]
                                                    }]
                                       },
                                      {'sector': 'nonprofits-index',
                                       'name': 'Grants and Contracts',
                                       'url_name': 'nonprofits-direct-expenditures',
                                       'children':[{ 'sector': 'nonprofits-direct-expenditures',
                                                     'name': 'Search Grants',
                                                     'url_name': 'nonprofits-faads-search',
                                                     'children':[]
                                       
                                                  },
                                                  { 'sector':'nonprofits-direct-expenditures',
                                                    'name': 'Search Contracts',
                                                    'url_name': 'nonprofits-fpds-search',
                                                    'children':[]
                                                    
                                                  }],
                                      },
                                      {'sector': 'nonprofits-index',
                                       'name': 'Tax Subsidies',
                                       'url_name': 'nonprofits-tax-expenditures',
                                       'children':[{'sector': 'nonprofits-tax-expenditures',
                                                      'name': 'Deduction for Charitable Contributions for Educational Institutions',
                                                      'url_name': 'nonprofits-tax-expenditures-edu-contrib',
                                                      'children':[]
                                                    },
                                                   {'sector': 'nonprofits-tax-expenditures',
                                                      'name': 'Deduction for Charitable Contributions for Health Organizations',
                                                      'url_name': 'nonprofits-tax-expenditures-health-contrib',
                                                      'children':[]
                                                    },
                                                    {'sector': 'nonprofits-tax-expenditures',
                                                      'name': 'Deduction for Charitable Contributions for Institutions Other than Education and Health',
                                                      'url_name': 'nonprofits-tax-expenditures-other-contrib',
                                                      'children':[]
                                                    },
                                                    {'sector': 'nonprofits-tax-expenditures',
                                                      'name': 'Credit Union Income',
                                                      'url_name': 'nonprofits-tax-expenditures-credit-union-income',
                                                      'children':[]
                                                    },
                                                    {'sector': 'nonprofits-tax-expenditures',
                                                      'name': 'Bonds for Private Nonprofit Educational Facilities',
                                                      'url_name': 'nonprofits-tax-expenditures-edu-bonds',
                                                      'children':[]
                                                    },
                                                     {'sector': 'nonprofits-tax-expenditures',
                                                      'name': 'Special BlueCross BlueShield Deduction',
                                                      'url_name': 'nonprofits-tax-expenditures-bcbs',
                                                      'children':[]
                                                    },
                                                    {'sector': 'nonprofits-tax-expenditures',
                                                      'name': 'Exclusion of Housing Allowances for Ministers',
                                                      'url_name': 'nonprofits-tax-expenditures-minister-housing',
                                                      'children':[]
                                                    },]
                                      },
                                      {'sector': 'nonprofits-index',
                                       'name': 'Loans & Loan Guarantees',
                                       'url_name': 'nonprofits-risk-transfers',
                                       'children':[]
                                      }
                          
                                    ]
                        },
                        { 'sector': 'energy-index',
                           'name': 'Energy',
                           'url_name': 'energy-index',
                           'children': [{'sector': 'energy-index',
                                          'name': 'Summary',
                                          'url_name': 'energy-overview',
                                          'children':[{'sector': 'energy-overview',
                                                       'name': 'Structure of the U.S. Energy Sector',
                                                       'url_name': 'energy-overview-structure',
                                                       'children':[]
                                                       },
                                                       {'sector': 'energy-overview',
                                                       'name': 'Limitations of Energy Sector Data',
                                                       'url_name': 'energy-overview-data-limitations',
                                                       'children':[]
                                                       }]
                                        },
                                        {'sector': 'energy-index',
                                          'name': 'Grants and Contracts',
                                          'url_name': 'energy-direct-expenditures',
                                          'children':[{'sector': 'energy-direct-expenditures',
                                                       'name': 'Search Grants',
                                                       'url_name': 'energy-faads-search',
                                                       'children':[]
                                                       },
                                                       {'sector': 'energy-direct-expenditures',
                                                       'name': 'Search Contacts',
                                                       'url_name': 'energy-fpds-search',
                                                       'children':[]
                                                       }]
                                        },
                                        {'sector': 'energy-index',
                                          'name': 'Tax Subsidies',
                                          'url_name': 'energy-tax-expenditures',
                                          'children':[]
                                        },
                                        {'sector': 'energy-index',
                                          'name': 'Loans & Loan Guarantees',
                                          'url_name': 'energy-risk-transfers',
                                          'children':[]
                                        },
                                        {'sector': 'energy-index',
                                          'name': 'Regulations',
                                          'url_name': 'energy-regulations',
                                          'children':[]
                                        }
                                    ]
                        }
                ]
            }
