//
//  ResultsViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/2/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "ResultsViewController.h"
#import "ViewController.h"
#import "DetailsViewController.h"

@interface ResultsViewController ()

@end

@implementation ResultsViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view from its nib.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

//MARK: IBactions
- (IBAction)okButton:(id)sender
{
    ViewController *cV = [[[ViewController alloc] initWithNibName:@"ViewController_iPhone" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [self viewDidUnload];
}

- (IBAction)foreheadButton:(id)sender
{
    DetailsViewController *cV = [[[DetailsViewController alloc] initWithNibName:@"DetailsViewController" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [self viewDidUnload];
    
}

@end
